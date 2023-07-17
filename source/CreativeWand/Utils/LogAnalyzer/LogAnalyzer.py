"""
LogAnalyzer.py

Contains utilities to parse log files.
"""
from typing import List
from typing import Callable

import json
import os

from CreativeWand.Utils.LogAnalyzer.LogItem import LogItem
from CreativeWand.Utils.Misc.FileUtils import relative_path
import numpy as np


class LogAnalyzer:
    def __init__(self, log_dir: str = None, include_subdir=False):
        """
        Initialize a LogAnalyzer class.
        :param include_subdir: whether to load files also from subdirectories.
        :param log_dir: If not None, load all logs from this directory and pre fill it.
        """
        self.log_dir = log_dir
        self.all_logs = []
        self.include_subdir = include_subdir
        if log_dir is not None:
            self.load_log_files_from_dir(log_dir, include_subdir=self.include_subdir)

    def load_log_files_from_dir(self, log_dir: str, include_subdir=None):
        """
        Helper function.
        Load log files and add them into self.all_logs.
        This can be used even if log files already exists (so as to load logs from more than 1 folder.)
        :param log_dir: directory where logs are from.
        :param include_subdir: whether to load files also from subdirectories.
        :return: None
        """
        if include_subdir is None:
            include_subdir = self.include_subdir
        for fn in self._list_files_in_dir(log_dir, include_subdir=include_subdir):
            log_item = LogItem(from_file=fn)
            self.all_logs.append(log_item)

    @staticmethod
    def _list_files_in_dir(log_dir: str, include_subdir=False) -> List[str]:
        """
        Get all files ending in .json from log_dir.
        :param log_dir: read logs from this directory.
        :param include_subdir: whether to load files also from subdirectories.
        :return: list of files to load.
        """
        file_list = []

        if include_subdir:
            for path, subdirs, files in os.walk(log_dir):
                for name in files:
                    file_list.append(os.path.join(path, name))
        else:
            for file in os.listdir(log_dir):
                if file.endswith(".json"):
                    file_list.append(os.path.join(log_dir, file))
        return file_list

    # region queries

    def filter_logs_by_query(self, query_func: Callable) -> list:
        """
        Return all log objects that makes `query_func` return True.
        :param query_func: query function to be used.
        :return: logs that fits.
        """
        result = []
        for item in self.all_logs:
            if query_func(item):
                result.append(item)
        return result

    def get_unique_logs_by_query(self, query_func: Callable, report_repeats=True) -> dict:
        """
        Get all unique objects (that returns different values with `query_func`).
        Only the first object (based on log loading order) will be returned.
        :param query_func: query function to be used.
        :param report_repeats: if True, print out a message when a repeat is detected.
        :return: a dictionary with key being returns from `query_func` and value being the log object.
        """
        result = {}
        for item in self.all_logs:
            value = query_func(item)
            if value in result:
                if report_repeats:
                    print(f"{value} appeared again for {item}! Ignoring.")
            else:
                result[value] = item
        return result

    def map_logs_by_query(self, query_func: Callable) -> list:
        """
        Get the result of applying `query_func` to all logs, getting a list of `[log_item, query_func(log_item)]`.
        :param query_func: query functino to be used.
        :return: a list of `[log_item, query_func(log_item)]`
        """
        result = []
        for item in self.all_logs:
            result.append([item, query_func(item)])
        return result

    # endregion

# Testing
if __name__ == '__main__':
    la = LogAnalyzer("Samples/")


    def test_filter(item: LogItem):
        return "test" in item.session_id


    def test_map(item: LogItem):
        return item.session_id


    assert len(la.filter_logs_by_query(test_filter)) == 1
    assert len(la.map_logs_by_query(test_map)) == 2

    print("test passed")
