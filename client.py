import base64
import logging
import time
from typing import Optional, Tuple, Union, Dict, Any, Mapping
import requests

# Configure logger for the API client
logger = logging.getLogger("APIClient")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class APIResponseError(Exception):
    """Custom exception raised when an API request fails a status check."""
    def __init__(self, response: requests.Response) -> None:
        self.status_code: int = response.status_code
        self.url: str = response.url
        self.body: str = response.text
        super().__init__(
            f"\n--- API Error ---\n"
            f"URL: {self.url}\n"
            f"Status Code: {self.status_code}\n"
            f"Response Body: {self.body}\n"
            f"-----------------"
        )

class APIClient:
    def __init__(
        self, 
        base_url: str, 
        auth_type: Optional[str] = None, 
        credentials: Optional[Union[str, Tuple[str, str]]] = None,
        api_key_header: str = "X-API-Key"
    ) -> None:
        self.base_url: str = base_url.rstrip("/")
        self.session: requests.Session = requests.Session()
        self.api_key_header: str = api_key_header
        
        if auth_type and credentials:
            self.set_auth(auth_type, credentials)

    def set_auth(self, auth_type: str, credentials: Union[str, Tuple[str, str]]) -> None:
        """Configure or switch authentication globally for the session."""
        normalized_auth_type: str = auth_type.lower()
        
        if normalized_auth_type == "bearer":
            self.session.headers["Authorization"] = f"Bearer {credentials}"
        elif normalized_auth_type == "basic":
            if isinstance(credentials, tuple):
                user, password = credentials
                encoded = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")
                self.session.headers["Authorization"] = f"Basic {encoded}"
            else:
                self.session.headers["Authorization"] = f"Basic {credentials}"
        elif normalized_auth_type == "api_key":
            self.session.headers[self.api_key_header] = str(credentials)
        else:
            raise ValueError(f"Unsupported auth_type: {auth_type}")

    def clear_auth(self) -> None:
        """Clear all active authentication headers."""
        self.session.headers.pop("Authorization", None)
        self.session.headers.pop(self.api_key_header, None)

    def request(
        self, 
        method: str, 
        endpoint: str, 
        auth_override: Optional[Dict[str, str]] = None,
        expect_status: Optional[int] = None,
        raise_on_error: bool = False,
        **kwargs: Any
    ) -> requests.Response:
        """
        Make an HTTP request with full type hints, optional middleware logging,
        context auth overrides, and automated validation.
        """
        url: str = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        headers: Dict[str, str] = self.session.headers.copy()
        kw_headers = kwargs.get("headers")
        if isinstance(kw_headers, Mapping):
            headers.update(dict(kw_headers))
        if auth_override:
            headers.update(auth_override)
        kwargs["headers"] = headers

        req_body: Optional[Any] = kwargs.get("json") or kwargs.get("data") or None

        logger.info(f"--> {method.upper()} {url}")
        if req_body:
            logger.debug(f"    Payload: {req_body}")

        start_time: float = time.time()
        response: requests.Response = self.session.request(method, url, **kwargs)
        elapsed_time: float = round((time.time() - start_time) * 1000, 2)

        logger.info(f"<-- {response.status_code} {method.upper()} {url} ({elapsed_time}ms)")
        logger.debug(f"    Response Body: {response.text}")

        if raise_on_error and not (200 <= response.status_code < 300):
            raise APIResponseError(response)
            
        if expect_status and response.status_code != expect_status:
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