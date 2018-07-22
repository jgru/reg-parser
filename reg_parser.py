__author__ = 'gru'

import logging
import argparse
from hive_manager import HiveManager


def init_logging():
    logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    logging.info("Logging set up completed")


if __name__ == "__main__":
    init_logging()
    ap = argparse.ArgumentParser(prog='reg-parser', description='A command '
                                                               'line tool to extract registry keys', epilog="Maintained by _|.62|_|")

    # Define optional arguments

    ap.add_argument("-r", "--raw", action="store_true", help="Print raw "
                                                             "values")
    ap.add_argument("-b", "--bare", action="store_true", help="Print bare "
                                                            "values (e.g. "
                                                            "for filtering "
                                                            "in XWays)")
    ap.add_argument("-t", "--treeStructure", action="store_true",
                    help="Print all keys")
    ap.add_argument("-o", "--output", nargs="?", help="Write result to file")

    ap.add_argument("-s", "--searchKeys", nargs="?",
                    help="Keys to search, maybe separated by commata without "
                         "whitespace")

    # Define positional argument
    ap.add_argument("input", help="path to hive (e.g. ~/tmp/NTUser.dat")
    args = ap.parse_args()

    # Define and init result
    result = ""

    # Create RegistryManager
    hive = HiveManager(args.input)

    if args.treeStructure:
        result = hive.get_tree_structure(hive.root, print_branch=True)
    print(result)
    # Process search keys
    sk = args.searchKeys.split(",")
    print("Keys to search: ", sk)
    if sk is not None:
        for s in sk:
            # Retrieve RecentDocs
            result += str(hive.retrieve(s, args.bare, args.raw))
    print(result)
    if args.output is not None:
        print("Write to: " + args.output)
        with open(args.output, "w+") as f:
            f.write(result)
