"""
OpeningMessage.py

Communication that sends kick-off messages.

This message only display once at the beginning of the session.
"""
from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req

opening_message = "I'm your Creative Wand, here to work together on writing a story with you." \
                  "\n\nYou will see a list of actions available to you." \
                  "\n\nTell me what you wish to do by typing in the word in the bracket." \
                  "\n\nOnce you selected an action, I will further guide you through each of it." \
                  "\n\nEnjoy the collaborative experience!" \
                  "" \
                  ""


class OpeningMessageComm(BaseCommunication):
    def __init__(self):
        super(OpeningMessageComm, self).__init__()
        self.description = "Let the Creative Wand introduce itself."

    def can_activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        if exp_manager.get_state("did_opening") is None:
            return True
        return False

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        exp_manager.frontend.send_information(Req(opening_message))
        exp_manager.set_state("did_opening", "yes")
