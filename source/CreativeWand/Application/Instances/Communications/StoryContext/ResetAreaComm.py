"""
ResetAreaComm.py

User asks for previously provided information on an area to be removed.

Contains a start range, an end range, and a topic.
"""

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class ResetAreaComm(BaseCommunication):
    def __init__(self):
        super(ResetAreaComm, self).__init__()
        self.description = "Reset what you did."

    def can_activate(self) -> bool:
        return True

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        exp_manager.frontend.send_information(Req("You can let me start fresh on part of the story."
                                                  "Specify an area and I will reset everything there for you."))

        while True:
            start = exp_manager.frontend.get_information(
                Req("Where (line number) should I start to clean up? ", cast_to=int))
            end = exp_manager.frontend.get_information(
                Req("Where (line number) should I stop cleaning up? ", cast_to=int))
            if start <= end:
                break
            else:
                exp_manager.frontend.send_information(
                    Req("Starting line number should be smaller than ending line number."))
        exp_manager.frontend.send_information(Req("OK."))
        exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="reset_area",
                range_start=int(start),
                range_end=int(end),
                content=None,
            )
        )
        topic_weights = exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="topic_weights"
            )
        )
        # exp_manager.frontend.send_information(Req("New topic weights: %s" % topic_weights))
        exp_manager.frontend.send_information(
            Req("Done! You can add things back to continue working."))

        return True
