import sys

from parser.parser import parse
from models.smt_creator import create_smt


def main():
    srs, names = parse(sys.argv[1])

    with open('tmp.smt2', 'w') as f:
        f.write(create_smt(srs, names))


if __name__ == '__main__':
    main()