from argparse import ArgumentParser
from .check import check_parse
from .execute import execute


def main():
    parser = ArgumentParser("OPUS CLI")
    subparsers = parser.add_subparsers(dest="subparser_name")

    check_parser = subparsers.add_parser("check", help="Check opuslang source code")
    check_parser.add_argument("file_name", help="opuslang file to check")
    check_parser.set_defaults(func=check_parse)

    execute_parser = subparsers.add_parser("execute")
    execute_parser.add_argument("file_name")

    args = parser.parse_args()

    if args.subparser_name == "check":
        check_parse(args.file_name)
    elif args.subparser_name == "execute":
        execute(args.file_name)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()