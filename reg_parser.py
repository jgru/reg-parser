#!/opt/conda/bin/python3

__author__ = 'gru'

import logging
import argparse
from hive_manager import HiveManager


def init_logging():
    logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    logging.info("Logging set up completed")


def str_sep():
    s = "\n\n\n"
    s += "===" * 10
    return s


if __name__ == "__main__":

    ap = argparse.ArgumentParser(prog='reg-parser', description='A command '
                                                               'line tool to extract registry keys', epilog="Maintained by _|.62|_|")
    # Define positional argument
    ap.add_argument("input", help="path to hive (e.g. ~/tmp/NTUser.dat)")

    # Define optional arguments
    ap.add_argument("-r", "--raw", action="store_true", help="Print raw "
                                                             "values")
    ap.add_argument("-b", "--bare", action="store_true", help="Print bare "
                                                            "content (e.g. "
                                                            "for filtering "
                                                            "in XWays)")
    ap.add_argument("-t", "--treeStructure", action="store_true",
                    help="Print all keys until specified depth")

    ap.add_argument("-o", "--output", nargs="?", help="Write result to file")

    ap.add_argument("-s", "--searchKeys", nargs="?",
                    help="Keys to search, may be separated by commata without "
                         "whitespace")

    ap.add_argument("-f", "--searchFragments", nargs="?",
                    help="Fragment/part of key to search, may be separated by commata without "
                         "whitespace")

    args = ap.parse_args()

    init_logging()
    # Define and init result
    result = ""

    # Create RegistryManager
    hive = HiveManager(args.input)
    result = ""
    if args.treeStructure:
        tree = hive.get_tree_structure(hive.root, print_branch=True)
        result += "[*] Hive tree"
        result += tree
        result += str_sep()

    # Process search keys
    if args.searchKeys is not None:
        sk = args.searchKeys.split(",")
        result += "\n[*] Keys to search: " + str(sk) + "\n"

        if sk is not None:
            for s in sk:
                # Retrieve RecentDocs
                result += str(hive.retrieve(s, args.bare, args.raw))

        result += str_sep()

    # Process search fragments
    if args.searchFragments is not None:
        sf = args.searchFragments.split(",")
        result += "\n[*] Key fragments to search: " + str(sf) + "\n"

        if sf is not None:
            for s in sf:
                # Search for fragments
                result += str(hive.search_key([hive.root], s))

    print(result)

    if args.output is not None:
        print("Write to: " + args.output)
        with open(args.output, "w+") as f:
            f.write(result)
