"""
StartExperiment.py

A universal entrypoint to define what systems to be available for experiments.
"""

import argparse
import json

from CreativeWand.Application.Instances.Frontend.WebFrontendHelper.WebFrontendServer import WebFrontendServer


class ExperienceHost:
    def __init__(self, config):
        if 'mode' in config:
            self.mode = config['mode']
        else:
            raise AttributeError("mode missing in config file.")
        if 'api_profile' in config:
            self.api_profile = config['api_profile']
        else:
            raise AttributeError("api_profile missing in config file.")

    def start_experiment(self):
        if self.mode == "story":
            story_mode_table = {
                "local": {"experience_manager_class_name": "ExperienceManager", "domain": "story",
                          "presets": "s1_local_only"},
                "global": {"experience_manager_class_name": "ExperienceManager", "domain": "story",
                           "presets": "s1_global_only"},
                "rl": {"experience_manager_class_name": "RLEM", "domain": "story", "presets": "s1_local_only"}
            }

            obj = WebFrontendServer(
                mode_table=story_mode_table,
                api_table=self.api_profile
            )
            obj.start_server(run_async=True)
        else:
            raise NotImplementedError
        print("Experiment Started")


default_config = {
    "mode": "story",
    "api_profile": {
        "gen": "local",
    }
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file_path', help="config file path", default="")
    args = parser.parse_args()
    path = args.config_file_path
    if len(path) >= 1:
        config_content = json.load(open(path, 'r'))
    else:
        config_content = default_config
    host = ExperienceHost(config=config_content)
    host.start_experiment()


if __name__ == '__main__':
    main()
