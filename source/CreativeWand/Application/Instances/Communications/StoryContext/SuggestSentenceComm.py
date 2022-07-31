"""
SuggestSentence.py

Communication that chooses a sentence from the document and suggests a sentence to follow it.
"""

import random

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseRequest as Req
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryContextQuery


class SuggestSentenceComm(BaseCommunication):
    def __init__(self):
        super(SuggestSentenceComm, self).__init__()
        self.description = "Give a starting point for a new direction in the story."
        self.topics = ["science", "sports", "food", "romance", "horror", "action"]

    def can_activate(self) -> bool:
        # can activate if there is at least one sentence in the document
        exp_manager = self.get_experience_manager()
        doc = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="get_document"))
        text = ""
        for line in doc:
            text += line + " "
        return len(text) > len(doc)

    def activate(self) -> bool:
        exp_manager = self.get_experience_manager()

        doc = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="get_document"))
        # topics = exp_manager.creative_context.execute_query(StoryContextQuery(q_type="topic_weights"))

        # choose a random sentence and topic from predefined list
        indices = range(len(doc))
        indices = filter(lambda i: len(doc[i]) > 0, indices)
        i = random.choice(list(indices))
        sentence = doc[i]
        topic = random.choice(self.topics)

        # generate a new sentence with chosen sentence as prompt
        exp_manager.frontend.send_information(Req("Loading..."))
        res = exp_manager.creative_context.execute_query(StoryContextQuery(
            q_type="generate_one",
            content={"prompt": sentence, "topics": {topic: 1.0}}
            )
        )

        # display
        exp_manager.frontend.send_information(Req("What if after sentence [%d] '%s', we had something like this about '%s': '%s'?" % (i, sentence, topic, res)))

        return True