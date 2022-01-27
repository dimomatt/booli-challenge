from typing import Dict, Any
import requests
import datetime 

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

def get_cves_from_last_n_days(n: int) -> Dict[str, Any]:
    # Get a json response from the cve database
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0/", params=get_timestamp_payload(n))
    return r.json()
