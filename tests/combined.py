#!/usr/bin/env python3
import argparse
import logging
from ipaddress import IPv4Address
from argparser_adapter import CommandLine, ArgparserAdapter, Choice, ChoiceCommand

petchoice = Choice("pet",False,default='cat',help="Pick your pet")
funchoice = Choice("fun",True,help="Pick your fun time")


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
    def hello(self):
        print("Hi!")

    @CommandLine()
    def binary(self, value: bool):
        """True or false"""
        print(value)

    @ChoiceCommand(funchoice)
    def morning(self,name:str='Truman'):
        print(f"morning {name}!")

    @ChoiceCommand(funchoice)
    def night(self):
        """dark"""
        print("it's dark")

    @ChoiceCommand(petchoice)
    def dog(self):
        """canine"""
        print("woof")

    @ChoiceCommand(petchoice)
    def cat(self,name:str='Morris'):
        """feline"""
        print(f"meow {name}")




def main():
    something = Something()
    adapter = ArgparserAdapter(something)
    #parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    adapter.register(parser)
    args = parser.parse_args()
    adapter.call_specified_methods(args)


if __name__ == "__main__":
    main()
