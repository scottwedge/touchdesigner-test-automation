import re
import importlib
import json
import sys
import os
import unittest
from pprint import pprint, pformat

CONFIG_PATH = "config.json"

__version__ = 0.1


def load_config(config_path=None):
    """load each line in config.txt into dictionary.

    :param config_path: <str> Path to config txt
    """
    config_dict = {}
    with open(config_path or CONFIG_PATH, "r") as config:

        config_dict = json.load(config)

    return config_dict


def _get_py_files(location):
    """Scan the location directory and return a list of .py filenames.
    scandir is reccomended for speed and handling of overlength Windows paths.

    :param location: <str> location to scan in.
    """
    py_files = []

    try:
        location = os.scandir(location)

    except OSError:
        print("The path:\n\t'{}'\ndoes not exist!\n".format(location))
        location = []

    for dir_entry in location:
        if dir_entry.is_file() and re.search(r"\.py$", dir_entry.name.lower()):
            py_files.append(dir_entry.name)

    return py_files


def run(config):
    """Import each python file detected in TESTS_LOCATION.

    :param config: containing info from config.txt.
    :type  config: dict
    """
    tests_location = config["tests_location"]
    log_name = config.get("log_name", "test_results.txt")

    sys.path.append(tests_location)

    test_results_log = os.path.join(tests_location, log_name)
    with open(test_results_log, "w+") as test_results_log:

        for path_to_py_file in _get_py_files(tests_location):

            py_file = os.path.splitext(path_to_py_file)[0]
            # import file as module
            test_module = importlib.import_module(
                py_file.replace("\\", "/"))

            # unittest
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(
                test_module.TestOpCreationMethods)
            test_results = unittest.TextTestRunner(verbosity=2).run(suite)
            print(str(test_results))
            # write results to log
            # test_results_log.write(
            #     "\tContents of {} module:\n".format(path_to_py_file))
            # test_results_log.write(str(test_results))

            # print results to user
            # print("\tresults:\n")
            # print(test_results.test_create_op())
            # pprint(dir(test_results))

    sys.path.remove(tests_location)

    return test_results_log


# load config from config.txt
CONFIG_DICT = load_config()
# run unit test launcher
TEST_RESULTS_LOG = run(CONFIG_DICT)

# exit Touch Designer, with optional callback
os.startfile(TEST_RESULTS_LOG.name)
# project.quit(force=True)
