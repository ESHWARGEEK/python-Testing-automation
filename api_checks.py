import urllib.request
import urllib.error
from retry import retry

@retry(max_attempts=3, delay=1)
def check_api_status(url: str) -> dict:
    """Makes a GET request to the given URL and returns status info."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            return {
                "status_code": response.getcode(),
                "ok": 200 <= response.getcode() < 300
            }
    except urllib.error.HTTPError as e:
        return {
            "status_code": e.code,
            "ok": False
        }
    except urllib.error.URLError as e:
        raise e
