'''
Entrypoint for CVE mapping app
'''
import argparse
import json
from lib.ingest import get_page_of_cves, get_cve_metadata_from_last_n_days
from lib.output import write_to_console, write_to_file
from lib.map import get_results_for_n_days

def main(inputs):
    if inputs.outfile is not None:
        write_to_file(get_results_for_n_days(120), inputs.outfile)
    else:
        write_to_console(get_results_for_n_days(120))

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Map from NVD to ECS fields")
    PARSER.add_argument("--outfile", "-o", type=str,
                        help="Optional output to file")
    PARSER.add_argument("--days", "-d", type=int, default=120,
                        help="Number of Days to gather data for. Default = 120")
    inputs=PARSER.parse_args()
    main(inputs)