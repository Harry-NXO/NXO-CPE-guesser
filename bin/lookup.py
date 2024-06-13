#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))
from lib.cpeguesser import CPEGuesser
from lib.utils import ManageSearch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find potential CPE names from a list of keyword(s) and return a JSON of the results"
    )
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        default="o",
        help="Specify the type of assets(o for Operating system, a for application, h for hardware).",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=2,
        help="Specify the number of result to return.",
    )
    parser.add_argument(
        "--version",
        "-v",
        type=str,
        default="",
        help="Give a string to match with corresponding asset version.",
    )
    parser.add_argument(
        "word",
        metavar="WORD",
        type=str,
        nargs="+",
        help="One or more keyword(s) to lookup",
    )
    args = parser.parse_args()
    cpeGuesser = CPEGuesser()
    sorted_list = cpeGuesser.guessCpe(args.word,args.type)
    searchManager= ManageSearch()
    best_matching_version=searchManager.search(sorted_list,args.type,args.word,args.version,args.limit)
    print(json.dumps(best_matching_version))
