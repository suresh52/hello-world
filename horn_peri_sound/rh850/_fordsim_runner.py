import re
import vlab
import glob
import logging
import argparse
import importlib

from common import _registered_classes


vlab.path.append(".")
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
RE_TEST_CASE = r"Test ID:(.*)"

# Import all the suites
# by importing all the test cases are registered
modules = glob.glob("*.py")
for module in modules:
    if module.startswith("suite"):
        importlib.import_module(module[:-3])


def execute_tests(args):  # noqa
    funcs = _get_by_name(args.testcase, _registered_classes.values())
    if not funcs:
        funcs = _get_by_id(args.testcase, _registered_classes.values())

    if not funcs:
        logging.error("No Test Case was found for : {}, Have you defined id and name properly?".format(args.testcase))
        raise

    if "before" in funcs:
        logging.info("Calling 'before' function")
        try:
            funcs["before"](args)
        except Exception as e:
            logging.error(repr(e))
            raise

    try:
        logging.info("Calling test case '{}'".format(funcs["test"].__name__))
        funcs["test"](args)
    except Exception as e:
        logging.error(repr(e))
        raise

    if "after" in funcs:
        try:
            funcs["after"](args)
        except Exception as e:
            logging.error(repr(e))
            raise

    vlab.exit()


def _get_by_name(name, classes):
    _funcs = {}
    for cls in classes:
        if name in cls.__dict__:
            # We found the function
            instance = cls()
            before = cls.__dict__.get('before', None)
            if before:
                _funcs['before'] = getattr(instance, "before")
            after = cls.__dict__.get('after', None)
            if after:
                _funcs["after"] = getattr(instance, "after")
            _funcs["test"] = getattr(instance, name)
    return _funcs


def _get_by_id(tc_id, classes):  # noqa

    def _sanitize_n_collect_test(ids, _cls, func_name):
        if ids:
            ids = m.group(1)
        else:
            return []

        ids = ids.strip().split()

        if tc_id not in ids:
            return []

        _funcs = {}
        instance = _cls()
        before = _cls.__dict__.get('before', None)
        if before:
            _funcs['before'] = getattr(instance, "before")
        after = cls.__dict__.get('after', None)
        if after:
            _funcs["after"] = getattr(instance, "after")
        _funcs["test"] = getattr(instance, name)
        return _funcs

    for cls in classes:
        for name, func in cls.__dict__.items():
            try:
                if callable(func) and func.__doc__:
                    m = re.search(RE_TEST_CASE, func.__doc__)
                    funcs = _sanitize_n_collect_test(m, cls, name)
                    if funcs:
                        return funcs
            except Exception:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--multi",
        "-m",
        action="store_true",
        help="Launch GHS Multi debugger"
    )
    parser.add_argument(
        "--gtest",
        action="store_true",
        help="Run google test simulation script"
    )
    parser.add_argument(
        "--elf",
        "-e",
        default=None,
        help="path of the ELF file to load to vlab.",
    )
    parser.add_argument(
        "--testcase",
        "-t",
        help="name of the test case to be run"
    )
    parser.add_argument(
        "--inputs",
        "-i",
        default=None,
        help="Input passed to the test."
    )
    parser.add_argument(
        "--outputs",
        "-o",
        default=None,
        help="Expected output passed to vlab tests"
    )

    args = parser.parse_args(__args__)  # noqa
    execute_tests(args)
