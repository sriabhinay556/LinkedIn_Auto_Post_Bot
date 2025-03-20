import random
import requests
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse

class ProxyCriteria:
    def __init__(
        self,
        anonymous: bool = True,
        countryset: Optional[Set[str]] = None,
        secure: bool = False,
        timeout: float = 5.0,
        max_proxies: int = 5
    ):
        self.anonymous = anonymous
        self.countryset = countryset or set()
        self.secure = secure
        self.timeout = timeout
        self.max_proxies = max_proxies

class ProxyRotator:
    def __init__(self, proxy_criteria: ProxyCriteria):
        self.proxy_criteria = proxy_criteria
        self.proxies: List[str] = []
        self.current_index = 0

    def refresh_proxies(self):
        """Fetch new proxies based on the criteria."""
        # Here you would implement the logic to fetch proxies
        # For this example, we'll use a placeholder
        self.proxies = self._fetch_proxies()
        random.shuffle(self.proxies)
        self.current_index = 0

    def _fetch_proxies(self) -> List[str]:
        """Placeholder method to fetch proxies."""
        # In a real implementation, you would use a proxy provider API or scrape free proxies
        # For this example, we'll return some dummy proxies
        return [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080",
            "http://proxy4.example.com:8080",
            "http://proxy5.example.com:8080",
        ][:self.proxy_criteria.max_proxies]

    def get_next_proxy(self) -> str:
        """Get the next proxy in the rotation."""
        if not self.proxies:
            self.refresh_proxies()
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

    def get_proxy_dict(self) -> Dict[str, str]:
        """Get the proxy dictionary for use with requests."""
        proxy = self.get_next_proxy()
        return {urlparse(proxy).scheme: proxy}

class RotatingIPSession(requests.Session):
    def __init__(self, proxy_rotator: ProxyRotator):
        super().__init__()
        self.proxy_rotator = proxy_rotator

    def request(self, method, url, *args, **kwargs):
        retries = 3
        for _ in range(retries):
            try:
                kwargs['proxies'] = self.proxy_rotator.get_proxy_dict()
                response = super().request(method, url, *args, **kwargs)
                if response.status_code != 403:
                    return response
            except requests.RequestException:
                continue
        
        # If all retries fail, raise the last exception
        raise requests.RequestException("Max retries reached. Unable to get a successful response.")

def create_rotating_ip_session(
    anonymous: bool = True,
    countryset: Optional[Set[str]] = None,
    secure: bool = False,
    timeout: float = 5.0,
    max_proxies: int = 5
) -> RotatingIPSession:
    """Create a RotatingIPSession with the specified criteria."""
    criteria = ProxyCriteria(anonymous, countryset, secure, timeout, max_proxies)
    rotator = ProxyRotator(criteria)
    return RotatingIPSession(rotator)

# Usage example
if __name__ == "__main__":
    session = create_rotating_ip_session(
        anonymous=True,
        countryset={"US", "GB"},
        secure=True,
        timeout=2.0,
        max_proxies=3
    )

    try:
        response = session.get("https://api.ipify.org?format=json")
        print(f"Request successful. IP: {response.json()['ip']}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
