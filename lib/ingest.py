'''
Functions to get input from the APIs
'''
from typing import Dict, Any, List
from math import ceil
import requests
import datetime 

MAX_PAGE_SIZE = 2000

def format_datetime(time_to_format: datetime.datetime) -> str:
    # This is maybe a silly helper, just formats to yyyy-MM-ddTHH:mm:ss:SSS
    # TODO: use actual UTC offset- in this case becuase we are looking for an interval
    # of 120 days, I don't actually think it matters
    return time_to_format.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")

def get_timestamp_payload(n: int) -> Dict[str, str]:
    # Get the current time and create a requests-ready payload
    curr_date = datetime.datetime.now()
    timedelta = datetime.timedelta(days=n)
    n_days_ago = curr_date - timedelta
    payload = {"pubStartDate": format_datetime(n_days_ago), "pubEndDate": format_datetime(curr_date)}
    return payload

def get_cve_metadata_from_last_n_days(n: int) -> Dict[str, Any]:
    # Get a json response from the cve database
    param = get_timestamp_payload(n).update({"resultsPerPage": 0})
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0/", params=param)
    return r.json()

def get_page_sizes(response: Any) -> List[int]:
    num_pages = ceil(response["totalResults"]/MAX_PAGE_SIZE)
    last_page_size = response[totalResults]%MAX_PAGE_SIZE
    page_size_list = [MAX_PAGE_SIZE] * num_pages
    page_size_list.append(last_page_size)
    return page_size_list

def get_page_n_of_cves(n: int, page_sizes: int, num_days: int) -> Any:
    request_params = {"startIndex": n * MAX_PAGE_SIZE, "resultsPerPage": MAX_PAGE_SIZE}
    request_params.update(get_timestamp_payload(int))
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0/", params=request_params)
    return r.json()

