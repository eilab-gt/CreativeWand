"""
UserWork.py

This communication allows the user to select one sentence
and replace it with one desired by them.

"""

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class UserWorkComm(BaseCommunication):
    def __init__(self):
        super(UserWorkComm, self).__init__()
        self.description = "Replace a sentence at a specific location."

    def can_activate(self) -> bool:
        # exp_manager = self.get_experience_manager()
        return True

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()

        existing_work = exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="get_document"
            )
        )
        # if len(existing_work) > 0:
        #     exp_manager.frontend.send_information(Req("Your work so far: "))
        #     for index, line in enumerate(existing_work):
        #         exp_manager.frontend.send_information(Req("[%d] %s" % (index, line)))
        # else:
        #     exp_manager.frontend.send_information(Req("Your work so far: None"))

        to_replace = exp_manager.frontend.get_information(Req("Which sentence number do you want to replace? "))
        index = int(to_replace)
        new_sentence = exp_manager.frontend.get_information(Req("Write your new text here: "))

        exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="force_one",
                content={"index": index, "sentence": new_sentence}
            )
        )

        exp_manager.set_state("just_forced_sentence", True)
