'''
Entrypoint for CVE mapping app
'''
import pandas as pd
import json
from cve import get_cves_from_last_n_days
from ecs_data import ECSData, populate_ECSData_from_json

ecs_fields = pd.read_csv("resources/ecs_fields.csv")
vuln_fields = [x for x in list(ecs_fields["Field"]) if "vulnerability" in x]


for cve_item in get_cves_from_last_n_days(120)["result"]['CVE_Items']:
    data_object = populate_ECSData_from_json(cve_item)
    print(data_object.asdict())