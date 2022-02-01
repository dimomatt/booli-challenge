'''
Functions to write output
'''
from lib.map import *

def write_to_file(thing_to_write: Any, output_file: str) -> None:
    with open(output_file, 'w') as outfile:
        outfile.write(thing_to_write)
    return

def write_to_console(thing_to_write: Any) -> None:
    # Making code more verbose is a good trait, right?
    # Really this is here in case I want to speed it up
    print(thing_to_write)


# These are in case I decide to become ambitious someday
def write_to_redis(thing_to_write: Any, redis_db: Any) -> None:
    return

def write_to_socket(thing_to_write: Any, host: str, host_port: int) -> None:
    return