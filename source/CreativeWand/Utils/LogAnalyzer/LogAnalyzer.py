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


# class LogAnalyzer:
#     def __init__(self, log_dir):
#         """
#         Initialize the instance.
#         :param log_dir: read logs from this directory.
#         """
#         log_files = self._list_files_in_dir(log_dir)
#         self.all_logs = {}
#         for fp in log_files:
#             this_record_obj = {'meta': {}, 'df': None}
#             json_obj = json.load(open(fp, 'r'))
#             sess_id = json_obj['session_id']
#             for key in json_obj:
#                 if key == "payload":
#                     df = pandas.DataFrame.from_dict(json_obj[key])
#                     this_record_obj['df'] = df
#                 else:
#                     this_record_obj['meta'][key] = json_obj[key]
#             self.all_logs[sess_id] = this_record_obj
#         print("Loaded %s logs. " % len(self.all_logs))
#
#     def _list_files_in_dir(self, log_dir) -> List[str]:
#         """
#         Get all files ending in .json from log_dir.
#         :param log_dir: read logs from this directory.
#         :return: list of files to load.
#         """
#         file_list = []
#         for file in os.listdir(log_dir):
#             if file.endswith(".json"):
#                 file_list.append(os.path.join(log_dir, file))
#         return file_list
#
#     def get_all_logs(self):
#         """
#         Get all logs.
#         :return: all logs.
#         """
#         return self.all_logs
#
#     def get_all_unique_participants(self):
#         """
#         Return a list of all unique participants (unique session_code).
#         :return: list of participants in their ids.
#         """
#         result = []
#         for item in self.all_logs:
#             if self.all_logs[item]['meta']['session_code'] not in result:
#                 result.append(self.all_logs[item]['meta']['session_code'])
#         return result
#
#     def find_by_session_id(self, sid):
#         """
#         Return specific log with session id.
#         :param sid: session id.
#         :return: specific log or None if not exist.
#         """
#         if sid in self.all_logs:
#             return self.all_logs[sid]
#         else:
#             return None
#
#     def find_by_session_code(self, sess_code):
#         """
#         Return all entries from a session code.
#         :param sess_code: sid to look for.
#         :return: all entries with this sid.
#         """
#         result = {}
#         for key, value in self.all_logs.items():
#             if value['meta']['session_code'] == sess_code:
#                 result[key] = value
#         return result
#
#     def pretty_print(self, sess_code):
#         this_log = self.find_by_session_code(sess_code)
#         print(this_log)
#
#     # def get_interactions_left(self, sid):
#     #     """
#     #     Get how many interaction is left in a session.
#     #     :param sid: id of session.
#     #     :return: interactions left.
#     #     """
#     #     interactions_left = 15  # max value
#     #     for item in self.all_logs[sid]['df']['args0']:
#     #
#     #         if "You have " in item and "interactions left" in item:
#     #             count = int(item.split(" ")[2])
#     #             # print(count)
#     #             if count < interactions_left:
#     #                 interactions_left = count
#     #         # print(item)
#     #     # print("FN:%s"%interactions_left)
#     #     return interactions_left
#     #
#     # def subgoal_completion(self, sid, subgoal_id):
#     #     """
#     #     How many interactions left
#     #     :param subgoal_id:
#     #     :return:
#     #     """
#     #     df = self.all_logs[sid]['df']
#     #     interactions_left = 15  # max value
#     #
#     #     for index, row in df.iterrows():
#     #         args0 = row['args0']
#     #         returned = row['returned']
#     #
#     #         if "You have " in args0 and "interactions left" in args0:
#     #             count = int(args0.split(" ")[2])
#     #             # print(count)
#     #             if count < interactions_left:
#     #                 interactions_left = count
#     #         elif "Which subgoal did we achieve?" in args0:
#     #             if subgoal_id in returned:
#     #                 # if interactions_left == 14:
#     #                 #     print(self.all_logs[sid]['meta']['session_code'])
#     #                 return interactions_left
#     #     return -1
#     #     # print(item)
#     #     # print("FN:%s"%interactions_left)
#
#     def specific_return_exist(self, sid, word):
#         """
#         Return if `word` exists in any of the returned results in a session.
#         Useful to capture feedbacks.
#         :param sid: session id.
#         :param word: word to look for.
#         :return:
#         """
#         for item in self.all_logs[sid]['df']['returned']:
#             if word.lower() in item.lower():
#                 return True
#         return False
#
#     def get_mode(self, sid):
#         """
#         Return experiment setup recorded in the metadata.
#         :param sid: session id.
#         :return: mode.
#         """
#         return self.all_logs[sid]['meta']['session_type']


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

    ###### LEGACY ######

    # valid_pid_list_fp = open(relative_path("../../../logs/valid_pid.txt"))
    # valid_pid_list = valid_pid_list_fp.readlines()
    # valid_pid_list = [line.rstrip() for line in valid_pid_list]
    # print(valid_pid_list)
    #

    #
    # all_participants = la.get_all_unique_participants()
    # print(all_participants)
    #
    # keywords = ["Satisfied", "Frustrated"]
    # keyword_found = {}
    # for item in keywords:
    #     keyword_found[item] = 0
    #
    # filter_mode = "global"
    # subgoal_achieved = {1: [], 2: [], 3: []}
    #
    # total_session = 0
    # provided_count = 0
    #
    # total_participant = 0
    #
    # for participant in all_participants:
    #     if participant not in valid_pid_list:
    #         print("Skipping %s, not finishing on prolific" % participant)
    #         continue
    #     participant_logs = la.find_by_session_code(participant)
    #     provided = False
    #     participant_counted = False
    #
    #     subgoal_this_participant = {}
    #     keyword_this_participant = []
    #
    #     for key in participant_logs:
    #         mode = la.get_mode(key)
    #         if filter_mode not in mode:
    #             continue
    #         interactions_left = la.get_interactions_left(key)
    #         if interactions_left >= 14:  # empty session
    #             continue  # skip very short sessions
    #         else:
    #             total_session += 1
    #             if not participant_counted:
    #                 participant_counted = True
    #                 total_participant += 1
    #
    #         for subgoal in [1, 2, 3]:
    #             result = la.subgoal_completion(key, str(subgoal))
    #             if 14 > result > 0:
    #                 if not provided:
    #                     provided_count += 1
    #                     provided = True
    #                 if subgoal not in subgoal_this_participant:  # no entry
    #                     subgoal_this_participant[subgoal] = result
    #                 elif subgoal_this_participant[subgoal] < result:  # we take the best
    #                     print("Same participant replace")
    #                     subgoal_this_participant[subgoal] = result
    #                 # subgoal_achieved[subgoal].append(result)
    #         # la.get_interactions_left(key)
    #
    #         for kw in keywords:
    #             if la.specific_return_exist(key, kw) and kw not in keyword_this_participant:
    #                 keyword_this_participant.append(kw)
    #                 keyword_found[kw] += 1
    #     for item in subgoal_this_participant:
    #         subgoal_achieved[item].append(subgoal_this_participant[item])
    #
    # print(subgoal_achieved)
    # print(keyword_found)
    # print("Provided = %s" % provided_count)
    # print("Total session = %s" % total_session)
    # print("Total participant = %s" % total_participant)
    # print("SG1: start business, SG2: end sports, SG3: have soccer")
    # for subgoal in [1, 2, 3]:
    #     print("Goal %s-avg=%s,std=%s" % (
    #         subgoal, np.average(subgoal_achieved[subgoal]), np.std(subgoal_achieved[subgoal])))

    #
    # la = LogAnalyzer(relative_path("../../../logs/logs_to_process/"))
    # al = la.all_logs
    #
    # keywords = ["Satisfied", "Frustrated"]
    # keyword_found = {}
    # for item in keywords:
    #     keyword_found[item] = 0
    #
    # filter_mode = "local"
    # subgoal_achieved = {1: [], 2: [], 3: []}
    #
    # total_session = 0
    # provided_count = 0
    # for key in al:
    #     provided = False
    #     mode = la.get_mode(key)
    #     if filter_mode not in mode:
    #         continue
    #     interactions_left = la.get_interactions_left(key)
    #     if interactions_left == 15:  # empty session
    #         continue  # skip very short sessions
    #     else:
    #         total_session += 1
    #
    #     for subgoal in [1, 2, 3]:
    #         result = la.subgoal_completion(key, str(subgoal))
    #         if result > 0:
    #             if not provided:
    #                 provided_count += 1
    #                 provided = True
    #             subgoal_achieved[subgoal].append(result)
    #     # la.get_interactions_left(key)
    #
    #     for kw in keywords:
    #         if la.specific_return_exist(key, kw):
    #             keyword_found[kw] += 1
    #
    # print(subgoal_achieved)
    # print(keyword_found)
    # print("Provided = %s" % provided_count)
    # print("Total session = %s" % total_session)
    # print("SG1: start business, SG2: end sports, SG3: have soccer")
    # for subgoal in [1, 2, 3]:
    #     print("Goal %s-avg=%s,std=%s" % (
    #     subgoal, np.average(subgoal_achieved[subgoal]), np.std(subgoal_achieved[subgoal])))
