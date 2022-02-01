'''
Functions to get input from the APIs
'''
from typing import Dict, Any, List
from math import ceil
import requests
import datetime 

MAX_PAGE_SIZE = 2000

def format_datetime(time_to_format: datetime.datetime) -> str:
    """formats datetime to the way the NVD api wants"""
    return time_to_format.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")

def get_timestamp_payload(n: int) -> Dict[str, str]:
    """Gets a correctly formatted dict for the pubstartdate and pubenddate"""
    curr_date = datetime.datetime.now()
    timedelta = datetime.timedelta(days=n)
    n_days_ago = curr_date - timedelta
    payload = {"pubStartDate": format_datetime(n_days_ago), "pubEndDate": format_datetime(curr_date)}
    return payload

def get_cve_metadata_from_last_n_days(n: int) -> Dict[str, Any]:
    """Get a simple response from the api containing metadata"""
    param = get_timestamp_payload(n)
    param["resultsPerPage"] = 0
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0/", params=param)
    return r.json()

def get_start_indices(response: Any) -> List[int]:
    """Get a list of indices representing the pages of CVEs to request"""
    total_results = response["totalResults"]
    last_page_size = response["totalResults"]%MAX_PAGE_SIZE
    start_index_list = []
    total_results -= last_page_size
    while total_results > 0:
        start_index_list.insert(0, total_results)
        total_results -= MAX_PAGE_SIZE
    start_index_list.insert(0,0)
    return start_index_list

def get_page_of_cves(start_index: int, num_days: int) -> Any:
    """Gets a page of cves given a start index and a number of days"""
    request_params = {"startIndex": start_index, "resultsPerPage": MAX_PAGE_SIZE}
    request_params.update(get_timestamp_payload(num_days))
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0/", params=request_params)
    return r.json()


