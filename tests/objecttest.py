#!/usr/bin/env python3
#
# Older version - Deprecated
#
import argparse
from ipaddress import IPv4Address
from argparser_adapter import ArgparserAdapter


class Something:

    def do_seven(self) -> int:
        print(7)
        return 7

    def do_double(self, x: int):
        """double a number"""
        print(2 * x)

    def do_sum(self, x: int, y: int):
        """sum arguments"""
        print(x + y)

    def do_triple(self, x):
        print(3 * int(x))

    def do_ipv4address(self, x: IPv4Address):
        print(x)

    def do_binary(self, value: bool):
        print(value)


def main():
    something = Something()
    adapter = ArgparserAdapter(something)
    something.argadapt_required = True
    parser = argparse.ArgumentParser()
    adapter.register(parser)
    args = parser.parse_args()
    adapter.call_specified_methods(args)


if __name__ == "__main__":
    main()
