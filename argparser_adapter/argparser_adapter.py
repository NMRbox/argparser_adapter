#!/usr/bin/env python3
import argparse
import configparser
import inspect
import logging
from typing import Any


class ArgparserAdapter:

    def __init__(self, *, prefix='do_', group=True, required=False):
        self.argadapt_prefix = prefix
        self.argadapt_required = required
        self.argadapt_group = group
        self._argadapt_dict = {}

    def param_conversion_exception(self, e: Exception, method_name: str, parameter_name: str, parameter_type: type,
                                   value: str) -> Any:
        """
        :param e: Exception thrown
        :param method_name: called method
        :param parameter_name: parameter name
        :param parameter_type:
        :param value: value passed on command line
        :return: valid value for parameter_type, or raise exception
        """
        raise ValueError(f"conversion error of method {method_name} parameter {parameter_name} value {value} {e}")

    def register(self, argparser: argparse.ArgumentParser) -> None:
        """Add arguments to argparser based on self.argadapt_settings"""
        needarg = False
        if self.argadapt_group:
            ap = argparser.add_mutually_exclusive_group(required=self.argadapt_required)
            arequired = False
            needarg = True
        else:
            ap = argparse
            arequired = self.argadapt_required
        plen = len(self.argadapt_prefix)
        for d in inspect.getmembers(self, self.__only_methods):
            name, mobj = d
            doc = inspect.getdoc(mobj)
            if name.startswith(self.argadapt_prefix):
                needarg = False
                arg = name[plen:]
                sig = inspect.signature(mobj)
                ptypes = [p for _, p in sig.parameters.items()]
                self._argadapt_dict[arg] = (getattr(self, name), ptypes)
                nargs = len(ptypes)
                if nargs > 0:
                    desc = tuple(sig.parameters.keys())
                    ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, required=arequired, help=doc)
                else:
                    ap.add_argument(f'--{arg}', action='store_true', help=doc)
        if needarg:
            raise ValueError(f"No methods staring with {self.argadapt_prefix} found and group is required")

    def call_specified_methods(self, args: argparse.Namespace) -> None:
        """Call method from parsed args previously registered"""
        for name, mspec in self._argadapt_dict.items():
            params = getattr(args, name, None)
            if params:
                method, iparams = mspec
                if params is True:  # noaction store_true argument
                    method()
                    return
                assert (len(params) == len(iparams))
                callparams = []
                for value, ptype in zip(params, iparams):
                    if ptype.annotation != ptype.empty:
                        try:
                            value = ptype.annotation(value)
                        except Exception as e:
                            value = self.param_conversion_exception(e, name, ptype.name, ptype.annotation, value)
                    callparams.append(value)
                method(*callparams)

    @staticmethod
    def __only_methods(x):
        return inspect.ismethod(x)
