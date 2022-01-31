'''
Entrypoint for CVE mapping app
'''
import argparse
import json
from cve import get_cves_from_last_n_days
from lib.output import write_to_console, write_to_file

main(inputs):
    if inputs.outfile:
        write_to_file(inputs.outfile)
    else:
        write_to_console()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Map from NVD to ECS fields")
    PARSER.add_argument("--outfile", "-o", type=str,
                        help="Optional output to file")
    inputs=PARSER.parse_args()
    main(inputs)