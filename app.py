'''
Entrypoint for CVE mapping app
'''
import argparse
import json
from lib.ingest import get_cves_from_last_n_days, get_num_pages_from_response
from lib.output import write_to_console, write_to_file
from lib.map import get_results_for_n_days

def main(inputs):
    print(get_num_pages_from_response(get_cves_from_last_n_days(120)))
    #if inputs.outfile:
    #    write_to_file(inputs.outfile)
    #else:
    #    write_to_console()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Map from NVD to ECS fields")
    PARSER.add_argument("--outfile", "-o", type=str,
                        help="Optional output to file")
    inputs=PARSER.parse_args()
    main(inputs)