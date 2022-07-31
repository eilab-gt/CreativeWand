"""
FeedbackComm.py

A base class for communications capturing experiment data.
"""

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req


class FeedbackComm(BaseCommunication):
    """
    Get free text response on specific questions.
    """

    def __init__(self, description, question_to_ask=""):
        super(FeedbackComm, self).__init__(description=description)
        self.question_to_ask = question_to_ask

    def can_activate(self) -> bool:
        return True

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        result = exp_manager.frontend.get_information(
            Req("The creative wand is wondering: %s" % self.question_to_ask))
        exp_manager.frontend.send_information(Req("You answered\"%s\". Thank you!" % result))
