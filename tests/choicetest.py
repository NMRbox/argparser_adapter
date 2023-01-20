#!/usr/bin/env python3
import argparse
import logging
from ipaddress import IPv4Address
from argparser_adapter import Choice,ChoiceCommand, ArgparserAdapter


petchoice = Choice("pet",False,default='cat',help="Pick your pet")
funchoice = Choice("fun",True,help="Pick your fun time")


class Something:

        
    @ChoiceCommand(funchoice)
    def morning(self):
        print("morning!")
        
    @ChoiceCommand(funchoice)
    def night(self):
        print("it's dark")
        
    @ChoiceCommand(petchoice)
    def dog(self):
        print("woof")

    @ChoiceCommand(petchoice)
    def cat(self):
        print("meow")



def main():
    something = Something()
    adapter = ArgparserAdapter(something, group=False, required=False)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    adapter.register(parser)
    args = parser.parse_args()
    adapter.call_specified_methods(args)


if __name__ == "__main__":
    main()
