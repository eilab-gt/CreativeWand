"""
RequestGeneration.py

Initiate the generation process.
"""
from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req


class GenerateComm(BaseCommunication):
    """
    (re)Generate using information gathered.
    """

    def __init__(self, no_sketch=False):
        super(GenerateComm, self).__init__()
        self.no_sketch = no_sketch
        self.description = "Start (re)generating the story."

    def can_activate(self) -> bool:
        # Always enable generation when no_sketch mode is up.
        if self.no_sketch: return True
        return self.get_experience_manager().creative_context.is_generation_ready()

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

        exp_manager.frontend.send_information(Req("OK, I'm generating parts that are not frozen..."))
        exp_manager.frontend.send_information(Req("Loading... (May take up to half a minute)"))
        generated_cache = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="generated_contents"))
        exp_manager.frontend.send_information(Req("Done!"))

        exp_manager.set_state("have_generated_once", True)
        return True


class GenerateWithFreezeComm(GenerateComm):
    """
    (re)Generate using information gathered, with frozen mask set.
    """

    def __init__(self, no_sketch=False):
        super(GenerateWithFreezeComm, self).__init__(no_sketch=no_sketch)
        self.description = "Set or remove freezing point and only regenerate from that point."

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        exp_manager.set_state("just_forced_sentence", False)
        hint = "You can freeze a sentence and every one before it and only regenerate the ones after it.\n Which sentence position? (-1 to disable and regenerate everything:)"
        start = exp_manager.frontend.get_information(Req(hint))
        exp_manager.frontend.send_information(Req("OK. Loading..."))
        exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="generate_freeze_after",
                range_start=int(start),
            )
        )
        generated_cache = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="generated_contents"))
        return True

    def can_activate(self) -> bool:
        # This can not be used when nothing is generated.
        if self.get_experience_manager().get_state("have_generated_once"):
            return True
        return False

    def confidence_to_interrupt_activate(self) -> float:
        confidence = 1.0 if self.get_experience_manager().get_state("just_forced_sentence") else 0.0
        print("Confidence interrupt: %s" % confidence)
        return confidence

    def suppress_interrupt(self):
        self.get_experience_manager().set_state("just_forced_sentence", False)
