#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Konrad <konrad.zdeb@me.com>
#
# Distributed under terms of the MIT license.

"""
This simple script provides a mechanism to run SPARQL files. The files are
sourced from within Python directory available in the package. The script reads
files as available in the provided folder and coffers convenient running
mechanism for all of the available files.
"""

###########
# Modules #
###########
import os
import argparse
from tabulate import tabulate


#############
# Functions #
#############
def check_directory(input_dir):
    """Check if directory exists and if it's not empty."""
    if not os.path.exists(input_dir):
        print("Error: provided path does not exist.")
        os._exit(1)
    if not os.path.isdir:
        print("Error: provided path is not a directory.")
        os._exit(1)
    if not os.listdir(input_dir):
        print("Error: provided directory is empty.")
        os._exit(1)


def list_query_files(input_dir, input_extensions):
    """List query files from the provided directory."""
    all_files = os.listdir(input_dir)
    # Filter to match files of desired extensions only
    query_files = filter(lambda x: os.path.splitext(x)[1] in input_extensions,
                         all_files)
    query_files = list(query_files)
    # Get full paths
    query_files = map(lambda x: os.path.join(input_dir, x), query_files)
    return query_files


def print_queries(query_files):
    """Print presentable table with list of queries and corresponding menu
    options."""
    print(tabulate({"File": map(lambda x: os.path.basename(x), query_files),
                    "Preview": map(lambda x: read_file(x, shorten=True),
                                   query_files)},
                   headers="keys", showindex="always",
                   tablefmt="psql"))


def read_file(input_file, shorten=False):
    """Read query file and optionally return preview line"""
    with open(input_file, 'r') as query_file:
        data = query_file.read().strip()
    # Optionaly produce shortened version
    if shorten:
        data = data[:30] + '...'
    return data


####################
# Arguments / run  #
####################
def run(args):
    """Main functions to run."""
    input_dir = args.input_dir
    input_extensions = args.input_extensions
    check_directory(input_dir)
    query_files = list_query_files(input_dir, input_extensions)
    print_queries(query_files)


def main():
    """Parse arguments and run main function."""
    parser = argparse.ArgumentParser(description="Simple program providing" +
                                     "very basic interface to SPARQL query" +
                                     "files.",
                                     prog="SPARQL runner",
                                     epilog="Konrad Zdeb @ GPL 3-0")
    parser.add_argument("-i", '--input_dir', help="Input directory with SPARQL query" +
                        "that %(prog)s will use to run queries.",
                        dest='input_dir', type=str, required=True)
    parser.add_argument('-e', '--extensions', help='File extensions to use' +
                        'defaults when searching for query files.',
                        dest='input_extensions', required=False,
                        nargs='+', type=str,
                        default=['.sql', '.txt', '.sparql'])
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
