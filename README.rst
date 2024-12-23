argparser_adapter
=================

This package provides automatic adding of arguments to an argparser. ArgumentParser
based on a simple method naming convention.

Basic Usage
-----------

Write your class with methods you wish called from a command line decorated with *@CommandLine()*
or *ChoiceCommand(choice)*
Create an **ArgparserAdapter**, passing your object as a constructor. Decorated methods
will be added to an argparser via the *register* call as positional or options. After parsing,
*call_specified_methods* will call methods specified on command. ArgparseAdapter will
attempt to convert command line strings to appropriate types if Python `type hints`_ are
provided.

Choice Options
--------------
Choice options are added by first creating a *Choice* instance and then adding a *ChoiceCommand* decorator for
each class method that should be a choice. The method name becomes a choice option for the specified choice. The
method docstring becomes part of the the help.

Choices may be positional or options, depending the value of the Choice *is_position* attribute. Default values
may be supplied.

CommandLine Options
~~~~~~~~~~~~~~~~~~~
Arguments may be designed as required using *@CommandLine(required=True).* Default values may
be specified with *@CommandLine(default=10).* Note specifying both required and a default is possible
but not useful.

Logging
~~~~~~~
Logging is to: **logging.getLogger('argparser_adapter')**

Example
~~~~~~~

::

    import argparse
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
            """The sun has risen"""
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

Note the *double* will receive a string and must convert it to an integer. The
type hint in *triple* ensures the argument will be an integer.

The resulting argument argparser help is:

::

    usage: combined.py [-h] [--binary value] [--double x] [--hello]
                       [--ipv4address x] [--seven] [--sum x y] [--triple x]
                       [--pet {cat,dog}]
                       {morning,night}

    positional arguments:
      {morning,night}  Pick your fun time
                       morning (The sun has risen)
                       night (dark)

    optional arguments:
      -h, --help       show this help message and exit
      --binary value   True or false
      --double x       double a number
      --hello
      --ipv4address x  Print ip address
      --seven
      --sum x y        sum arguments
      --triple x       triple a value
      --pet {cat,dog}  Pick your pet
                       cat (feline)
                       dog (canine)

Docstrings, if present, become help arguments.

Advanced usage
______________
When type conversion fails, the method

::

    def param_conversion_exception(self, e: Exception, method_name: str, parameter_name: str, parameter_type: type,
                                   value: str) -> Any:

is called. The default behavior is to raise a ValueError_ exception including the method and parameter names, the value
passed and the original exception message. This method is provided for subclasses to override,
if desired. An implementation should raise an Exception or return a suitable parameter for
calling *method_name*.

Alternative packages
--------------------
More complete packages are available for this purpose, such as Click_. This implementation is
intended to be simple, lightweight and easy to use.

.. _type hints: https://docs.python.org/3/library/typing.html
.. _ValueError: https://docs.python.org/3/library/exceptions.html#ValueError
.. _Click: https://click.palletsprojects.com/

