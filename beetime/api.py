import json
from urllib.parse import urlencode

import requests
from requests.compat import urljoin

BASE_URL = "https://www.beeminder.com/api/v1/"

def _get_query_body(token: str) -> dict:
    return {
        "auth_token": token
    }
    
def _get_query_headers() -> dict:
    return {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
    }
    

def get_user(username: str, token: str) -> None:
    url = urljoin(BASE_URL, f"users/{username}.json")
    
    headers = _get_query_headers()
    data = urlencode(_get_query_body(token))
    
    response = requests.request("GET", url, headers=headers, data=data)

    response.raise_for_status()
    
    return


def send_datapoints_of_goal(user, token, slug, data, did=None):
    """Send or update a datapoint to a given Beeminder goal. If a
    datapoint ID (did) is given, the existing datapoint is updated.
    Otherwise a new datapoint is created. Returns the datapoint ID
    for use in caching.
    """
    response = api_call("POST", user, token, slug, data, did)
    return json.loads(response)["id"]


def api_call(method, user, token, slug, data, did):
    """Prepare an API request.

    Based on code by: muflax <mail@muflax.com>, 2012
    """

    cmd = "datapoints"
    base = urljoin(BASE_URL, f"users/{user}/goals/{slug}/")
    if method == "POST" and did is not None:
        url = urljoin(base, f"{cmd}/{did}.json")
        method = "PUT"
    else:
        url = urljoin(base, f"{cmd}.json")

    headers = _get_query_headers()
    data = urlencode(_get_query_body(token) if method == "GET" else data)

    response = requests.request(method, url, headers=headers, data=data)
    response.raise_for_status()
    return response.text
