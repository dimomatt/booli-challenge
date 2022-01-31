'''
Function to map fields from the CVE API to the output
'''
from lib.ingest import get_page_n_from_cves

#ecs_fields = pd.read_csv("resources/ecs_fields.csv")
#vuln_fields = [x for x in list(ecs_fields["Field"]) if "vulnerability" in x]


#for cve_item in get_cves_from_last_n_days(120)["result"]['CVE_Items']:
#    data_object = populate_ECSData_from_json(cve_item)
#    print(data_object.asdict())

def get_ecs_json():
    return