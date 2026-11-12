from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout))
    )
    def get(self, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, **kwargs)