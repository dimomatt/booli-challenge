'''
Function to map fields from the CVE API to the output
'''
from typing import Dict, Any
from lib.ingest import get_page_n_of_cves, get_num_pages_from_response, get_cves_from_last_n_days

#ecs_fields = pd.read_csv("resources/ecs_fields.csv")
#vuln_fields = [x for x in list(ecs_fields["Field"]) if "vulnerability" in x]


#for cve_item in get_cves_from_last_n_days(120)["result"]['CVE_Items']:
#    data_object = populate_ECSData_from_json(cve_item)
#    print(data_object.asdict())


def fill_vuln_fields(nvd_response: Dict[str, Any]):
    return

def get_ecs_json(Dict[str, Any]) -> Dict[str, Any]:
    return