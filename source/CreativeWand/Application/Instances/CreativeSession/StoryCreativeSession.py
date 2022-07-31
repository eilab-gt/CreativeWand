"""
SimpleCreativeSession.py

(Formerly RunInActiveMode.py)

Some functions to let experience manager form a complete loop.
These scripts provide standalone way to use the experience manager
in a co-creative session.

Other frontend can also use ExperienceManager as a utility, thus
avoiding using this script.
"""
from CreativeWand.Application.Instances.Communications.FeedbackComm import FeedbackComm
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery
from CreativeWand.Application.Instances.Frontend.WebFrontendHelper.WebFrontendSessionManager import \
    SessionEndedException
from CreativeWand.Framework.CreativeSession.BaseCreativeSession import BaseCreativeSession
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
import time


def is_yes(reply: str) -> bool:
    """
    Check if a string means "yes".
    :param reply: user reply.
    :return: Is it "yes".
    """

    if "y" in reply or "Y" in reply:
        return True
    return False


class StoryCreativeSession(BaseCreativeSession):

    def record_log_item(self, log_item) -> None:
        pass

    def start_session(self) -> None:
        self.manager.frontend.set_log_keywords(['request', 'info', 'doc'])
        turn_count = 15
        timer_enabled = True
        while True:
            try:
                doc, sketches = self.refresh_manager_states()
                self.manager.frontend.set_doc(doc, sketches)
            except:
                print("Trying to send docs to frontend before round but failed.")
            self.manager.save_logs()
            if timer_enabled:
                self.manager.frontend.send_information(Req("You have %s interactions left." % turn_count))
                turn_count -= 1
                if turn_count < 0:
                    self.manager.frontend.send_information(
                        Req("Experiment ends here. Thank you for your participation. You will be rediected to end page in 10 seconds."))
                    time.sleep(10)
                    self.manager.frontend.send_kill_to_react()
                    break
            try:
                if self.manager.wish_to_interrupt_with_preferred():
                    result = self.manager.frontend.get_information(
                        Req("The creative wand want to suggest something. Is it OK? (yes/no)"))
                    if type(result) is str and is_yes(result):
                        success = self.manager.activate_preferred()
                        if success:
                            continue
                    else:
                        self.manager.suppress_all_interrupts()
                list_of_comms = self.manager.get_list_of_available_communications_for_user()
                text_to_display = "The creative wand is waiting for you to take the next action. \n === Available ===\n"
                index = -1
                for item in list_of_comms:
                    index += 1
                    text_to_display = text_to_display + "[%s]%s\n" % (index, item.description)
                text_to_display = text_to_display + "[-1]We're done!\nWhich option? (Number in [])"
                result = self.manager.frontend.get_information(Req(text_to_display, cast_to=int))
                if result in range(len(list_of_comms)):
                    # If providing feedback, refund the turn count.
                    if type(list_of_comms[result]) == FeedbackComm:
                        turn_count += 1
                    self.manager.interrupt_activate(list_of_comms[result])
                elif result < 0:
                    self.manager.frontend.send_information(Req("Thank you for using!%s" % turn_count))
                    self.manager.frontend.send_kill_to_react()
                    break
                else:
                    self.manager.frontend.send_information(
                        Req("The Wand doesn't know what to do with your input, try again."))

                doc, sketches = self.refresh_manager_states()


            except Exception as e:
                print("Exception: %s" % e)
                print("Type: %s" % type(e))
                if type(e) is SessionEndedException:
                    self.end_session()
                    return
                self.manager.frontend.send_information(
                    Req("Sorry, I can't understand what you are saying. Would you mind trying again?"))

            # try:
            #     self.manager.frontend.set_doc(doc, sketches)
            # except:
            #     print("Trying to send docs to frontend after round but failed.")

        self.end_session()

    def refresh_manager_states(self):
        doc = self.manager.creative_context.document
        sketches = self.manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="get_all_sketches"
            )
        )
        return doc, sketches

    def end_session(self):
        self.manager.save_logs()
