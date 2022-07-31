"""
UserProvideSketch.py

User provides a sketch so as to influence the geneerated stories.

Sketches contains a start range, an end range, and a topic.
"""
from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class UserSketchComm(BaseCommunication):
    """
    The communication that asks user information on a sketch, and then apply it to the Story creative context.
    """

    def __init__(self):
        super(UserSketchComm, self).__init__()
        self.description = "Provide a sketch to guide the generation process."

    def can_activate(self) -> bool:
        return True

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        exp_manager.frontend.send_information(Req("You can let me introduce a specific topic to part of the story."
                                                  "Just let me know the topic and where to apply."))
        topic_message = "Which topic should I introduce? Try one from %s or yours:" % exp_manager.creative_context.suggested_topics
        topic = exp_manager.frontend.get_information(Req(topic_message))

        # Bugfix: make topic lower cased so generator recognizes it
        if type(topic) is str:
            topic = topic.lower().capitalize()

        while True:
            start = exp_manager.frontend.get_information(
                Req("Where (line number) should I phase this topic in? ", cast_to=int))
            end = exp_manager.frontend.get_information(
                Req("Where (line number) should I phase this topic out? ", cast_to=int))
            if start <= end:
                break
            else:
                exp_manager.frontend.send_information(
                    Req("Starting line number should be smaller than ending line number."))
        exp_manager.frontend.send_information(Req("OK."))
        exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="sketch",
                range_start=int(start),
                range_end=int(end),
                content=topic,
            )
        )
        topic_weights = exp_manager.creative_context.execute_query(
            StoryContextQuery(
                q_type="topic_weights"
            )
        )
        # exp_manager.frontend.send_information(Req("New topic weights: %s" % topic_weights))
        exp_manager.frontend.send_information(
            Req("You've added a sketch for topic %s! You can add more, or see updated stories by asking me to show "
                "the stories again!" % topic))

        return True
