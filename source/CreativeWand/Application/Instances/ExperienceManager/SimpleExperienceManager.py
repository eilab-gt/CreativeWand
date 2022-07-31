"""
SimpleExperienceManager.py

Describe the baseline "simple" experience manager.
"""
import time

from CreativeWand.Application.Instances.Frontend.CommandLineFrontend import CommandLineFrontend
from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryCreativeContext
from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext

from CreativeWand.Application.Instances.Communications.FeedbackComm import FeedbackComm
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery
from CreativeWand.Application.Instances.Frontend.WebFrontendHelper.WebFrontendSessionManager import \
    SessionEndedException
from CreativeWand.Framework.ExperienceManager.BaseExperienceManager import BaseExperienceManager
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req

from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseFrontend


def is_yes(reply: str) -> bool:
    """
    Check if a string means "yes".
    :param reply: user reply.
    :return: Is it "yes".
    """

    if "y" in reply or "Y" in reply:
        return True
    return False


class SimpleExperienceManager(BaseExperienceManager):
    frontend: BaseFrontend

    def __init__(
            self,
            creative_context: BaseCreativeContext = None,
            frontend: BaseFrontend = None,
            info: dict = None,
    ):
        super(SimpleExperienceManager, self).__init__(creative_context=creative_context, frontend=frontend, info=info)

        if self.frontend is None:
            # Set default
            self.frontend = CommandLineFrontend()
        """
        Frontend used. In this case just printing and input().
        """

        self.creative_context: StoryCreativeContext

    def interrupt_activate(self, comm: BaseCommunication) -> bool:
        return comm.activate()

    def wish_to_interrupt_with_preferred(self) -> bool:
        return len(self.comm_group_manager.get_interrupt_communications()) > 0

    def activate_preferred(self) -> bool:
        if len(self.comm_group_manager.get_interrupt_communications()) > 0:
            self.comm_group_manager.get_interrupt_communications()[0].activate()
            return True
        else:
            return False

    def get_list_of_available_communications_for_user(self) -> list:
        return self.comm_group_manager.get_available_communications()

    def start_session(self) -> None:
        self.frontend.set_log_keywords(['request', 'info', 'doc'])
        turn_count = 15
        timer_enabled = True
        while True:
            try:
                self.refresh_manager_states()
                doc = self.get_state("doc")
                sketches = self.get_state("sketches")
                self.frontend.set_doc({"document": doc, "sketch": sketches})
            except:
                print("Trying to send docs to frontend before round but failed.")
            self.save_logs()
            if timer_enabled:
                self.frontend.send_information(Req("You have %s interactions left." % turn_count))
                turn_count -= 1
                if turn_count < 0:
                    self.frontend.send_information(
                        Req("Experiment ends here. Thank you for your participation. You will be rediected to end page in 10 seconds."))
                    time.sleep(10)
                    self.frontend.send_kill_to_react()
                    break
            try:
                if self.wish_to_interrupt_with_preferred():
                    result = self.frontend.get_information(
                        Req("The creative wand want to suggest something. Is it OK? (yes/no)"))
                    if type(result) is str and is_yes(result):
                        success = self.activate_preferred()
                        if success:
                            continue
                    else:
                        self.suppress_all_interrupts()
                list_of_comms = self.get_list_of_available_communications_for_user()
                text_to_display = "The creative wand is waiting for you to take the next action. \n === Available ===\n"
                index = -1
                for item in list_of_comms:
                    index += 1
                    text_to_display = text_to_display + "[%s]%s\n" % (index, item.description)
                text_to_display = text_to_display + "[-1]We're done!\nWhich option? (Number in [])"
                result = self.frontend.get_information(Req(text_to_display, cast_to=int))
                if result in range(len(list_of_comms)):
                    # If providing feedback, refund the turn count.
                    if type(list_of_comms[result]) == FeedbackComm:
                        turn_count += 1
                    self.interrupt_activate(list_of_comms[result])
                elif result < 0:
                    self.frontend.send_information(Req("Thank you for using!%s" % turn_count))
                    self.frontend.send_kill_to_react()
                    break
                else:
                    self.frontend.send_information(
                        Req("The Wand doesn't know what to do with your input, try again."))

                self.refresh_manager_states()
                doc = self.get_state("doc")
                sketches = self.get_state("sketches")

            except Exception as e:
                print("Exception: %s" % e)
                print("Type: %s" % type(e))
                if type(e) is SessionEndedException:
                    self.end_session()
                    return
                self.frontend.send_information(
                    Req("Sorry, I can't understand what you are saying. Would you mind trying again?"))

            # try:
            #     self.manager.frontend.set_doc(doc, sketches)
            # except:
            #     print("Trying to send docs to frontend after round but failed.")

        self.end_session()

    def refresh_manager_states(self):
        doc = self.creative_context.document
        sketches = self.creative_context.execute_query(
            StoryContextQuery(
                q_type="get_all_sketches"
            )
        )
        self.set_state("doc", doc)
        self.set_state("sketches", sketches)
        # return doc, sketches

    def end_session(self):
        self.save_logs()
