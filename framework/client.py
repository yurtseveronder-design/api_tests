"""The single HTTP client used by every test.

Features: timeouts, retries with exponential backoff, bearer / basic / API-key
auth, per-request header overrides, request logging with timing, and optional
status assertions that raise a readable error.
"""

import base64
import logging
import time
from typing import Any, Dict, Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import ConnectTimeoutError, ReadTimeoutError
from urllib3.util.retry import Retry

from framework.config import DEFAULT_TIMEOUT, USER_AGENT

logger = logging.getLogger("api_tests.client")

# Only idempotent methods are retried: replaying a POST could create duplicates.
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})
RETRY_STATUSES = (500, 502, 503, 504)

Credentials = Union[str, Tuple[str, str]]


class APIResponseError(Exception):
    """Raised when a response fails a status expectation."""

    def __init__(self, response: requests.Response, expected: Optional[int] = None) -> None:
        self.status_code = response.status_code
        self.url = response.url
        self.body = response.text
        expectation = f"expected {expected}" if expected else "expected 2xx"
        super().__init__(
            f"{expectation}, got {self.status_code} from {self.url}\n"
            f"Response body: {self.body[:500]}"
        )


class APIClient:
    def __init__(
        self,
        base_url: str,
        auth_type: Optional[str] = None,
        credentials: Optional[Credentials] = None,
        api_key_header: str = "X-API-Key",
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.api_key_header = api_key_header

        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            status=retries,
            backoff_factor=backoff_factor,
            status_forcelist=RETRY_STATUSES,
            allowed_methods=IDEMPOTENT_METHODS,
            raise_on_status=False,  # hand back the final 5xx response instead of raising
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        if auth_type and credentials:
            self.set_auth(auth_type, credentials)

    # -- auth -------------------------------------------------------------
    def set_auth(self, auth_type: str, credentials: Credentials) -> None:
        kind = auth_type.lower()
        if kind == "bearer":
            self.session.headers["Authorization"] = f"Bearer {credentials}"
        elif kind == "basic":
            if isinstance(credentials, tuple):
                raw = f"{credentials[0]}:{credentials[1]}".encode("utf-8")
                credentials = base64.b64encode(raw).decode("ascii")
            self.session.headers["Authorization"] = f"Basic {credentials}"
        elif kind == "api_key":
            self.session.headers[self.api_key_header] = str(credentials)
        else:
            raise ValueError(f"Unsupported auth_type: {auth_type}")

    def clear_auth(self) -> None:
        self.session.headers.pop("Authorization", None)
        self.session.headers.pop(self.api_key_header, None)

    # -- requests ---------------------------------------------------------
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        expect_status: Optional[int] = None,
        raise_on_error: bool = False,
        **kwargs: Any,
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        start = time.perf_counter()
        try:
            response = self.session.request(method.upper(), url, **kwargs)
        except requests.exceptions.ConnectionError as exc:
            # requests reports a timeout as ConnectionError once retries are used up;
            # surface it as the Timeout type callers expect.
            reason = getattr(exc.args[0], "reason", None) if exc.args else None
            if isinstance(reason, ReadTimeoutError):
                raise requests.exceptions.ReadTimeout(str(exc), request=exc.request) from exc
            if isinstance(reason, ConnectTimeoutError):
                raise requests.exceptions.ConnectTimeout(str(exc), request=exc.request) from exc
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("%s %s -> %s (%.0f ms)", method.upper(), url, response.status_code, elapsed_ms)

        if expect_status is not None and response.status_code != expect_status:
            raise APIResponseError(response, expect_status)
        if raise_on_error and not response.ok:
            raise APIResponseError(response)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    # -- lifecycle --------------------------------------------------------
    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
