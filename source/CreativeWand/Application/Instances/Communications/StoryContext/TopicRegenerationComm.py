"""
TopicRegeneration.py

Communication that gives a topic to the user and asks for a range of sentences to change the topics.
"""

import random

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class TopicRegenerationComm(BaseCommunication):
    def __init__(self):
        super(TopicRegenerationComm, self).__init__()
        self.description = "Give a topic to change a portion of the story."

    def can_activate(self) -> bool:
        # can activate if there is an existing sketch with at least two topics
        exp_manager = self.get_experience_manager()
        topics = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="topic_weights"))
        return len(topics) >= 2

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()
        topics = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="topic_weights"))

        # choose a random topic (TODO: eventually, do something smarter that can suggest entirely new topics)
        topic, weights = random.choice(list(topics.items()))
        exp_manager.frontend.send_information(Req("Let's use the topic '%s' somewhere." % topic))

        # ask for a start and end sentence
        start = exp_manager.frontend.get_information(
            Req("Where (line number) should I phase this topic in? ", cast_to=int))
        end = exp_manager.frontend.get_information(
            Req("Where (line number) should I phase this topic out? ", cast_to=int))

        # update the sketch
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
        return True
