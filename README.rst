argparser_adapter
=================

This calls provides automatic adding of arguments to an argparser.ArgumentParser
based on a simple method naming convention.

Basic Usage
-----------

Derive your class from **ArgparserAdapter**. Methods starting with a prefix will
be added to an argparser via the *register* call as -- arguments. After parsing,
*call_specified_methods* will call methods specified on command. ArgparseAdapter will
attempt to convert command line strings to appropriate types if Python `type hints`_ are
provided.

Example
~~~~~~~

::

    import argparse
    from ipaddress import IPv4Address
    from argparse_adapter.argparse_adapter import ArgparserAdapter

    class Something(ArgparserAdapter):

        def do_seven(self)->int:
            print(7)
            return 7


        def do_double(self,x):
            """double a number"""
            print(2*int(x))

        def do_triple(self,x:int):
            print(3*x)

        def do_sum(self,x:int,y:int):
            """sum arguments"""
            print(x + y)

        def do_ipv4address(self,x:IPv4Address):
            print(x)


    def main():
        something = Something()

Note the do_double will receive a string and must convert it to an integer. The
type hint in do_triple ensures the argument will be an integer.

The resulting argument argparser help is:

::

    usage: objecttest.py [-h]
                         (--double x | --ipv4address x | --seven | --sum x y | --triple x)

    optional arguments:
      -h, --help       show this help message and exit
      --double x       double a number
      --ipv4address x
      --seven
      --sum x y        sum arguments
      --triple x

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

