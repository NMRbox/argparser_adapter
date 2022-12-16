#!/usr/bin/env python3
import argparse
import logging
from ipaddress import IPv4Address

from argparser_adapter import ArgparserAdapter
from argparser_adapter.argparser_adapter import CommandLine


class Something:

    @CommandLine()
    def seven(self) -> int:
        # no help for this argument
        print(7)
        return 7

    @CommandLine()
    def double(self, x: int):
        """double a number"""
        print(2 * x)

    @CommandLine()
    def sum(self, x: int, y: int):
        """sum arguments"""
        print(x + y)

    @CommandLine(default=10)
    def triple(self, x: int):
        """triple a value"""
        print(3 * int(x))

    @CommandLine()
    def ipv4address(self, x: IPv4Address):
        """Print ip address"""
        print(type(x))
        print(x)

    @CommandLine()
    def binary(self, value: bool):
        """True or false"""
        print(value)

    @CommandLine(required=True)
    def happy(self, v: str):
        """Report how happy we are"""
        print(f"Happy is {v}")


def main():
    something = Something()
    adapter = ArgparserAdapter(something, group=False, required=False)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    adapter.register(parser)
    args = parser.parse_args()
    adapter.call_specified_methods(args)


if __name__ == "__main__":
    main()
