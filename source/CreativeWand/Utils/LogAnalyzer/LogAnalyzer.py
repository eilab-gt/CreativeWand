"""
LogAnalyzer.py

Contains utilities to parse log files.
"""
from typing import List

import pandas
import json
import os
from CreativeWand.Utils.Misc.FileUtils import relative_path
import numpy as np


class LogAnalyzer:
    def __init__(self, log_dir):
        """
        Initialize the instance.
        :param log_dir: read logs from this directory.
        """
        log_files = self._list_files_in_dir(log_dir)
        self.all_logs = {}
        for fp in log_files:
            this_record_obj = {'meta': {}, 'df': None}
            json_obj = json.load(open(fp, 'r'))
            sess_id = json_obj['session_id']
            for key in json_obj:
                if key == "payload":
                    df = pandas.DataFrame.from_dict(json_obj[key])
                    this_record_obj['df'] = df
                else:
                    this_record_obj['meta'][key] = json_obj[key]
            self.all_logs[sess_id] = this_record_obj
        print("Loaded %s logs. " % len(self.all_logs))

    def _list_files_in_dir(self, log_dir) -> List[str]:
        """
        Get all files ending in .json from log_dir.
        :param log_dir: read logs from this directory.
        :return: list of files to load.
        """
        file_list = []
        for file in os.listdir(log_dir):
            if file.endswith(".json"):
                file_list.append(os.path.join(log_dir, file))
        return file_list

    def get_all_logs(self):
        """
        Get all logs.
        :return: all logs.
        """
        return self.all_logs

    def get_all_unique_participants(self):
        """
        Return a list of all unique participants (unique session_code).
        :return: list of participants in their ids.
        """
        result = []
        for item in self.all_logs:
            if self.all_logs[item]['meta']['session_code'] not in result:
                result.append(self.all_logs[item]['meta']['session_code'])
        return result

    def find_by_session_id(self, sid):
        """
        Return specific log with session id.
        :param sid: session id.
        :return: specific log or None if not exist.
        """
        if sid in self.all_logs:
            return self.all_logs[sid]
        else:
            return None

    def find_by_session_code(self, sess_code):
        """
        Return all entries from a session code.
        :param sess_code: sid to look for.
        :return: all entries with this sid.
        """
        result = {}
        for key, value in self.all_logs.items():
            if value['meta']['session_code'] == sess_code:
                result[key] = value
        return result

    def get_interactions_left(self, sid):
        """
        Get how many interaction is left in a session.
        :param sid: id of session.
        :return: interactions left.
        """
        interactions_left = 15  # max value
        for item in self.all_logs[sid]['df']['args0']:

            if "You have " in item and "interactions left" in item:
                count = int(item.split(" ")[2])
                # print(count)
                if count < interactions_left:
                    interactions_left = count
            # print(item)
        # print("FN:%s"%interactions_left)
        return interactions_left

    def subgoal_completion(self, sid, subgoal_id):
        """
        How many interactions left
        :param subgoal_id:
        :return:
        """
        df = self.all_logs[sid]['df']
        interactions_left = 15  # max value

        for index, row in df.iterrows():
            args0 = row['args0']
            returned = row['returned']

            if "You have " in args0 and "interactions left" in args0:
                count = int(args0.split(" ")[2])
                # print(count)
                if count < interactions_left:
                    interactions_left = count
            elif "Which subgoal did we achieve?" in args0:
                if subgoal_id in returned:
                    # if interactions_left == 14:
                    #     print(self.all_logs[sid]['meta']['session_code'])
                    return interactions_left
        return -1
        # print(item)
        # print("FN:%s"%interactions_left)

    def specific_return_exist(self, sid, word):
        """
        Return if `word` exists in any of the returned results in a session.
        Useful to capture feedbacks.
        :param sid: session id.
        :param word: word to look for.
        :return:
        """
        for item in self.all_logs[sid]['df']['returned']:
            if word.lower() in item.lower():
                return True
        return False

    def get_mode(self, sid):
        """
        Return experiment setup recorded in the metadata.
        :param sid: session id.
        :return: mode.
        """
        return self.all_logs[sid]['meta']['session_type']


# Testing
if __name__ == '__main__':

    valid_pid_list_fp = open(relative_path("../../../logs/valid_pid.txt"))
    valid_pid_list = valid_pid_list_fp.readlines()
    valid_pid_list = [line.rstrip() for line in valid_pid_list]
    print(valid_pid_list)

    la = LogAnalyzer(relative_path("../../../logs/logs_to_process/"))
    al = la.all_logs

    all_participants = la.get_all_unique_participants()
    print(all_participants)

    keywords = ["Satisfied", "Frustrated"]
    keyword_found = {}
    for item in keywords:
        keyword_found[item] = 0

    filter_mode = "global"
    subgoal_achieved = {1: [], 2: [], 3: []}

    total_session = 0
    provided_count = 0

    total_participant = 0

    for participant in all_participants:
        if participant not in valid_pid_list:
            print("Skipping %s, not finishing on prolific" % participant)
            continue
        participant_logs = la.find_by_session_code(participant)
        provided = False
        participant_counted = False

        subgoal_this_participant = {}
        keyword_this_participant = []

        for key in participant_logs:
            mode = la.get_mode(key)
            if filter_mode not in mode:
                continue
            interactions_left = la.get_interactions_left(key)
            if interactions_left >= 14:  # empty session
                continue  # skip very short sessions
            else:
                total_session += 1
                if not participant_counted:
                    participant_counted = True
                    total_participant += 1

            for subgoal in [1, 2, 3]:
                result = la.subgoal_completion(key, str(subgoal))
                if 14 > result > 0:
                    if not provided:
                        provided_count += 1
                        provided = True
                    if subgoal not in subgoal_this_participant:  # no entry
                        subgoal_this_participant[subgoal] = result
                    elif subgoal_this_participant[subgoal] < result:  # we take the best
                        print("Same participant replace")
                        subgoal_this_participant[subgoal] = result
                    # subgoal_achieved[subgoal].append(result)
            # la.get_interactions_left(key)

            for kw in keywords:
                if la.specific_return_exist(key, kw) and kw not in keyword_this_participant:
                    keyword_this_participant.append(kw)
                    keyword_found[kw] += 1
        for item in subgoal_this_participant:
            subgoal_achieved[item].append(subgoal_this_participant[item])

    print(subgoal_achieved)
    print(keyword_found)
    print("Provided = %s" % provided_count)
    print("Total session = %s" % total_session)
    print("Total participant = %s" % total_participant)
    print("SG1: start business, SG2: end sports, SG3: have soccer")
    for subgoal in [1, 2, 3]:
        print("Goal %s-avg=%s,std=%s" % (
            subgoal, np.average(subgoal_achieved[subgoal]), np.std(subgoal_achieved[subgoal])))

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
