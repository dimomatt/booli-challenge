import json
import os
from lib.output import *

def test_file_writing():
    """Confirm that writing a file writes what I want"""
    list_of_dicts = [{"test": 2}, {"test": "3.0"}]
    write_to_file(list_of_dicts, "test.txt")
    with open("test.txt") as inputfile:
        assert inputfile.readlines()[0] == str(list_of_dicts)
    # cleanup
    os.remove("test.txt")

