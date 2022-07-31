"""
StoryPresets.py

preset objects (communications, creative context, etc.) for story domain.
"""

from CreativeWand.Application.Instances.Communications.Echo import EchoComm
from CreativeWand.Application.Instances.Communications.FeedbackComm import FeedbackComm
from CreativeWand.Application.Instances.Communications.OpeningMessage import OpeningMessageComm
from CreativeWand.Application.Instances.Communications.StoryContext.InspirationComm import InspirationComm
from CreativeWand.Application.Instances.Communications.StoryContext.RequestGeneration import GenerateComm, \
    GenerateWithFreezeComm
from CreativeWand.Application.Instances.Communications.StoryContext.ResetAreaComm import ResetAreaComm
from CreativeWand.Application.Instances.Communications.StoryContext.ShowGenerated import ShowGeneratedComm
from CreativeWand.Application.Instances.Communications.StoryContext.SuggestSentenceComm import SuggestSentenceComm
from CreativeWand.Application.Instances.Communications.StoryContext.TopicRegenerationComm import TopicRegenerationComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserProvideSketch import UserSketchComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserWorkComm import UserWorkComm
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryCreativeContext
from CreativeWand.Application.Instances.ExperienceManager.SimpleExperienceManager import SimpleExperienceManager
from CreativeWand.Application.Instances.Frontend.WebFrontend import WebFrontend

class_name_to_type = {
    "ExperienceManager": SimpleExperienceManager,
    "Frontend": WebFrontend,
    "CreativeContext": StoryCreativeContext,
}

comm_list_objects = {"OpeningMessageComm": OpeningMessageComm, "EchoComm": EchoComm,
                     "FeedbackComm": [FeedbackComm, dict(description="Tell us how you feel right now.",
                                                         question_to_ask="Do you feel (Satisfied) or (Frustrated) or something else at this moment?"
                                                         )], "UserSketchComm": UserSketchComm,
                     "ShowGeneratedComm": ShowGeneratedComm, "GenerateWithSketchComm": ShowGeneratedComm,
                     "GenerateComm": GenerateComm, "GenerateWithFreezeComm": GenerateWithFreezeComm,
                     "GenerateComm_nosketch": [GenerateComm, dict(no_sketch=True)],
                     "GenerateWithFreezeComm_nosketch": [GenerateWithFreezeComm, dict(no_sketch=True)],
                     "UserWorkComm": UserWorkComm, "InspirationComm": InspirationComm,
                     "TopicRegenerationComm": TopicRegenerationComm, "SuggestSentenceComm": SuggestSentenceComm,
                     "ResetAreaComm": ResetAreaComm,
                     "FeedbackSubgoalAchieved": [FeedbackComm, dict(
                         description="Report to us on achieving subgoals.",
                         question_to_ask="Which subgoal did we achieve? (1 to 3, or None)?"
                     )]}

comm_list_presets = {
    "test": comm_list_objects.keys(),
    "s1_local_only": [
        "OpeningMessageComm",
        "FeedbackComm",
        # "ResetAreaComm",
        "FeedbackSubgoalAchieved",
        "GenerateComm_nosketch",
        "GenerateWithFreezeComm_nosketch",
        "UserWorkComm",
    ],
    "s1_global_only": [
        "OpeningMessageComm",
        "FeedbackComm",
        #"ResetAreaComm",
        "FeedbackSubgoalAchieved",
        "UserSketchComm",
        "GenerateWithSketchComm",

    ],

}


def create_comms_from_preset(name: str) -> list:
    """
    Instantiate all communications based on the name for the preset.
    :param name: preset name.
    :return: all instantiated communications (Still needs bi
    """
    result = []
    try:
        comm_list = get_preset(name)
    except KeyError:
        raise KeyError("Unknown preset for exp_setup: %s" % exp_setup)
    if comm_list is not None:
        for item in comm_list:
            result.append(o(item))
    return result
    # sem.register_communication(o(item))
    # print("Registered: Frontend # %s" % sem.frontend.id)


def get_preset(name: str) -> list:
    """
    Get a preset communication list from the preset dictionary.
    :param name: key for the comm list.
    :return: the comm list.
    """
    return comm_list_presets[name]


def o(name: str) -> object:
    """
    Get an object from comm_list_objects.
    :param name: key
    :return: value
    """
    entry = comm_list_objects[name]
    if type(entry) is list:
        result = entry[0](**entry[1])
    else:
        result = entry()
    print("Created object: %s" % result)
    return result

# def get_story_creative_session(id, frontend, comm_list=None, exp_setup=None, em_info=None):
#     """
#     Get a new instance SimpleExperienceManager, encapsulaed in a CreativeSession.
#     exp_setup and comm_list can not be set at the same time.
#     :param em_info: Any additional info to pass to the experience manager.
#     :param exp_setup: (str) name of the experience setup, to be used to retrieve a preset.
#     :param id: unique identifier for the manager.
#     :param frontend: frontend to be plugged into.
#     :param comm_list: List of communications to be used. If None, a default list of comms will be used.
#     :return: a StoryCreativeSession object.
#     """
#     info = {"session_id": id, "session_type": exp_setup}
#     if em_info is not None:
#         for key in em_info:
#             info[key] = em_info[key]
#     sem = SimpleExperienceManager(frontend=frontend, info=info)
#     sem.bind_creative_context(StoryCreativeContext())
#     if comm_list is not None and exp_setup is not None:
#         raise AttributeError("comm_list and exp_setup can not be both set for get_story_creative_session")
#     if exp_setup is not None:
#         try:
#             comm_list = get_preset(exp_setup)
#         except KeyError:
#             raise KeyError("Unknown preset for exp_setup: %s" % exp_setup)
#     if comm_list is not None:
#         for item in comm_list:
#             sem.register_communication(o(item))
#             print("Registered: Frontend # %s" % sem.frontend.id)
#     else:
#         raise AttributeError("Unknown setup specified.")
#         # print("Using default communication list.")
#         # sem.register_communication(OpeningMessageComm())
#         # sem.register_communication(EchoComm())
#         # sem.register_communication(UserSketchComm())
#         # sem.register_communication(ShowGeneratedComm())
#         # sem.register_communication(GenerateComm())
#         # sem.register_communication(GenerateWithFreezeComm())
#         # sem.register_communication(UserWorkComm())
#         # sem.register_communication(InspirationComm())
#         # sem.register_communication(TopicRegenerationComm())
#         # sem.register_communication(SuggestSentenceComm())
#     # sess = StoryCreativeSession(manager=sem)
#     return sem
