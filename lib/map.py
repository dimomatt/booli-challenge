'''
Function to map fields from the CVE API to the output
'''
import os
import pwd
import datetime
from typing import Dict, List, Any
from lib.ingest import get_start_indices, get_page_of_cves, get_cve_metadata_from_last_n_days


def fill_vuln_fields(ecs_item: Dict[str, Any],
                     cve: Dict[str, Any]) -> Dict[str, Any]:
    """Populate the "vulnerability" fields that are mapable"""
    vuln_items = {}
    # Base Vuln Fields
    vuln_items["classification"] = "cvssV3"
    vuln_items["description"] = cve["cve"]["description"]
    vuln_items["enumeration"] = "CVE"
    vuln_items["id"] = cve["cve"]["CVE_data_meta"]["ID"]
    vuln_items["reference"] = cve["cve"]["references"]["reference_data"][0]["url"]
    vuln_items["severity"] =  cve["impact"]["base_metricV3"]["cvssV3"]["baseSeverity"]
    
    # Score Fields
    score = {}
    score["base"] = cve["impact"]["base_metricV3"]["cvssV3"]["baseScore"]
    score["version"] = cve["impact"]["baseMetricV3"]["cvssV3"]["version"]
    
    # Putting it all together
    vuln_items["score"] = score
    ecs_item["vulnerability"] = vul_items
    return ecs_item

def fill_ecs_fields(ecs_item: Dict[str, any],
                    cve: Dict[str, Any]) -> Dict[str, Any]:
    """Populate the ECS fields"""
    ecs_fields = {}
    ecs_item["ECS"] = ecs_fields
    return ecs_item

def fill_base_fields(ecs_item: Dict[str, any],
                     cve: Dict[str, Any]) -> Dict[str, Any]:
    """Populate the Base fields of a given ecs_item"""
    ecs_version = "8.2.0-dev"
    ecs_item["@timestamp"] = cve["publishedDate"]
    ecs_item["ECS.version"] = ecs_version
    ecs_item["tags"] = cve["cve"]["references"]["reference_data"][0]["tags"]
    return ecs_item



def fill_event_fields(ecs_item: Dict[str, any],
                      cve: Dict[str, Any]) -> Dict[str, Any]:
    """populates the "event" fields for a given ecs item"""
    event = {}
    event["action"] = "cve-data-update"
    event["agent_id_status"] = "auth_metadata_missing"
    event["category"] = "web"   
    event["created"] = cve["publishedDate"]
    event["dataset"] = "nist.nvd_api"
    event["ingested"] = datetime.datetime.now()
    event["severity"] = cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
    event["kind"] = "enrichment"
    event["provider"] = "NIST"
    event["reason"] = "regular lookup"
    event["reference"] = cve["cve"]["references"]["reference_data"][0]["url"]
    event["risk_score"] = cve["impact"]["baseMetricV3"]["impactScore"]
    ecs_item["event"] = event
    return ecs_item


def get_username() -> str:
    """Gets the username of the person running this program"""
    # https://stackoverflow.com/questions/842059/is-there-a-portable-way-to-get-the-current-username-in-python
    return pwd.getpwuid( os.getuid() )[ 0 ]

def fill_related_fields(ecs_item: Dict[str, any],
                        cve: Dict[str, Any]) -> Dict[str, Any]:
    """Fills the "related" fields of a given ecs_item"""
    related = {}
    related["user"] = get_username()
    ecs_item["related"] = related
    return ecs_item

def get_cve_url(cve_id: "str") -> str:
    """Gets a url for info regarding a specific CVE"""
    return f"https://services.nvd.nist.gov/rest/json/cve/1.0/{cve_id}"

def fill_service_fields(ecs_item: Dict[str, any],
                        cve: Dict[str, Any]) -> Dict[str, Any]:
    """Fill the "Service" fields"""
    service = {}
    service["address"] = get_cve_url(cve["cve"]["CVE_data_meta"]["ID"])
    service["type"] = "web"
    ecs_item["service"] = service
    return ecs_item

def get_ecs_json(nvd_item: Dict[str, Any]) -> Dict[str, Any]:
    """Gets the ecs json for a single CVE"""
    output = {}
    # Sometimes these fail on a missing field, we don't want to crash the whole thing
    extractors = [fill_base_fields,
                  fill_ecs_fields,
                  fill_event_fields,
                  fill_related_fields,
                  fill_service_fields,
                  fill_vuln_fields]
    for extractor in extractors:
    # Sometimes these fail on a missing field, we don't want to crash the whole thing
        try:
            extractor(output, nvd_item)
        except KeyError:
            continue
    return output

def get_ecs_for_start_index(start_index: int, num_days: int) -> List[Dict[str, Any]]:
    """Get a filled out list of ECS items for a page of CVE's, given a start index and number of days"""
    response = get_page_of_cves(start_index, num_days)
    output = []
    for item in response["result"]["CVE_Items"]:
        output.append(get_ecs_json(item))
    return output

def get_results_for_n_days(n: int) -> List[Dict[str, Any]]:
    """Gets a list of ECS json for all CVE's from n days ago"""
    result = []
    start_indices = get_start_indices(get_cve_metadata_from_last_n_days(n))
    for page_size in start_indices:
        result += get_ecs_for_start_index(start_indices, n)
    return result

