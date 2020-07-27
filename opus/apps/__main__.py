from argparse import ArgumentParser
from .check import check_parse


def main():
    parser = ArgumentParser("OPUS CLI")
    subparsers = parser.add_subparsers(dest="subparser_name")

    check_parser = subparsers.add_parser("check", help="Check opuslang source code")
    check_parser.add_argument("file_name", help="opuslang file to check")
    check_parser.set_defaults(func=check_parse)

    args = parser.parse_args()

    if args.subparser_name == "check":
        check_parse(args.file_name)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()