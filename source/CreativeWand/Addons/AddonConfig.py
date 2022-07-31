"""
AddonConfig.py

This file stores interface definitions for all tools in the toolbox.
"""

"""
Note: DO NOT add .py to filename used in "file" field, as they are used
by string concatenation to form python import paths.
"""

# Here we included some sample

tool_config = {
    "sample": {
        "file": "Sample",
        "class": "SampleTool",
        "func": None,
    },
    "pnb": {
        "file": "PNB.endpoint",
        "class": "PNBTool",
        "func": None,
        "config": {
            "base_location": "/mnt/hdd/trained_models/skill_model/ROC-large_v201",
            "gedi_location": "/mnt/hdd/trained_models/gedi_base/gedi_topic/",
        }
    },
    "pnb-gptj": {
        "file": "PNB.endpoint",
        "class": "PNBTool",
        "func": None,
        "config": {
            "slurm": "yep",  # anything works here, this triggers routines for gpt-j
            "gedi_location": "/home/gpu_sudo/projects/creative-wand/models/gedi/gedi_topic",
        }
    },

}
