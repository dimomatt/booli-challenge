'''
Function to map fields from the CVE API to the output
'''
from typing import Dict, Any
from lib.ingest import get_page_sizes, get_page_n_of_cves



def fill_vuln_fields(nvd_response: Dict[str, Any]) -> Dict[str, Any]:
    return

def fill_other_fields(nvd_response: Dict[str, Any]) -> Dict[str, Any]:
    return

def get_ecs_json(nvd_response: Dict[str, Any]) -> Dict[str, Any]:
    response = {}
    response.update(fill_vuln_fields(nvd_response))
    response.update(fill_other_fields(nvd_response))
    return response

def get_ecs_for_page(page_size: int):
    return get_ecs_json(get_page_n_of_cves())


def get_results_for_n_days(n: int) -> Dict[str, Any]:
    page_sizes = get_page_sizes(get_cve_metadata_from_last_n_days(n))
    return map(get_ecs_for_page, page_sizes)
