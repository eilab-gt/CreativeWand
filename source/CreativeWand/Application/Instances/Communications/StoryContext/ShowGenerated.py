"""
ShowGenerated.py

The agent provides generated sentences to the user.
"""
from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class ShowGeneratedComm(BaseCommunication):
    """
    Show generated sentences.
    """

    def __init__(self):
        super(ShowGeneratedComm, self).__init__()
        self.description = "Show/Update generated sentences."

    def can_activate(self) -> bool:
        return self.get_experience_manager().creative_context.is_generated_contents_ready()

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()

        should_regenerate = exp_manager.creative_context.execute_query(
            StoryContextQuery(q_type="get_should_regenerate"))
        if not should_regenerate:
            result = exp_manager.frontend.get_information(
                Req("You haven't make any changes. Do you want me to just try regenerating again? (yes/no)"))
            if result.lower() == "yes":
                exp_manager.creative_context.execute_query(
                    StoryContextQuery(q_type="reset_should_regenerate"))

        exp_manager.frontend.send_information(Req("Loading... (Will take up to half a minute)"))
        generated_cache = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="generated_contents"))
        exp_manager.frontend.send_information(Req("Done! Check the new story."))
        # exp_manager.frontend.send_information(Req("Here's the generated story:"))
        # for item in generated_cache:
        #     exp_manager.frontend.send_information(Req("%s" % item))
        return True
