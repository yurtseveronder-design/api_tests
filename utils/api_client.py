import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logging.info(f"Sending {method} request to: {url}")
        response = self.session.request(method, url, **kwargs)
        logging.info(f"Received status code: {response.status_code} from {url}")
        return response