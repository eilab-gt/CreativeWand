"""
StoryCreativeContext.py

This file contains interface to connect with the story generator.
"""

from CreativeWand.Application.Config.CreativeContextConfig import available_configs, available_carp_configs
from CreativeWand.Application.Utils.StorySketch import StorySketchManager
from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext, ContextQuery
from CreativeWand.Utils.Network.RemoteAPI import RemoteAPIInterface

default_connection_profile = "local"

default_carp_connection_profile = "local"


# region api calls

def call_generation_interface(
        prompt: str,
        topic: dict,
        connection_profile=None,
):
    """
    Utility function to call remote generation interface.
    :param prompt: the sentence to be continued.
    :param topic: topic weights used for generation.
    :param connection_profile: endpoint used to call remote API.
    :return: sentence generated from remote API.
    """

    if connection_profile is None:
        connection_profile = default_connection_profile

    default_server_addr = available_configs[connection_profile]["default_server_addr"]
    generate_api_route = available_configs[connection_profile]["generate_api_route"]

    call_result = RemoteAPIInterface.request(
        method="POST",
        address="%s%s" % (default_server_addr, generate_api_route),
        data={"skill": 0,
              "sentence": prompt,
              "topic": topic, "task": "generation"}
    )

    if call_result.success:
        # Retrieve just the generated sentences.
        # return call_result.payload['out']['out_sentence'] #legacy
        return call_result.payload['out_sentence']
    else:
        raise RuntimeError("Failed to call API: %s" % call_result.payload)

# endregion


class StoryContextQuery(ContextQuery):
    """
    Context query specific to story creative context.
    """

    def __init__(self,
                 prompt: str = None,
                 q_type: object = None,
                 content: object = None,
                 description: str = None,
                 range_start=0,
                 range_end=0):
        """
        Create a new story context query.
        :param range_start: start of range to apply this query to
        :param q_type: type of this query.
        :param range_end: end of range to apply this query to
        :param content: Topic to be used, or exact sentence.
        :param description:
        """
        super(StoryContextQuery, self).__init__()

        # Defines range to apply this query to
        self.range_start = range_start
        self.range_end = range_end

        # Topic to be used
        self.type = q_type
        self.content = content

        self.prompt = prompt

        # Additional messages (human readable, for debugging)
        self.description = description


class StoryCreativeContext(BaseCreativeContext):
    """
    Story generator context.
    """

    def __init__(self,
                 sentence_count=10,
                 initial_prompt="Here is a story from a story book for children. Once upon a time, ",
                 suggested_topics=None,
                 api_profile=None,
                 ):
        """
        Initialize this story generator.
        :param sentence_count: Count of sentence to be generated per each story.
        """
        super(StoryCreativeContext, self).__init__()

        if suggested_topics is None:
            self.suggested_topics = ["Business", "Science", "World", "Sports"]
        else:
            self.suggested_topics = suggested_topics
        self.gaussian_var = 1

        if api_profile is None:
            self.gen_api_profile = default_connection_profile
        else:
            self.gen_api_profile = api_profile["gen"]
        print(api_profile)
        print("API for generation: %s" % self.gen_api_profile)

        """
        Internal variables for interpreting sketches.
        """

        self.sentence_count = sentence_count
        """
        Count of sentence to be generated per each story.
        """

        self.document = []
        self.freeze_mask = [False] * self.sentence_count
        """
        Generated sentences cached. Can be invalidated.
        """
        self.reset_document()

        self.initial_prompt = initial_prompt
        """
        Initial prompt used in the story generation routine (generate()).
        """

        # Internal switch used to indicate whether we need to regenerate,
        # because the parameters used to generate story had changed.
        self.should_regenerate = True

        # Information we need to collect to generate sentences for this context
        self.prompt = "Prompt stub"
        self.topic_weight = {}

        self.sketch_manager = StorySketchManager(sentence_count=self.sentence_count, gaussian_var=self.gaussian_var)

    def execute_query(self, query: StoryContextQuery) -> object:
        """
        Execute a query so as to update internal information,
        :param query: Query.
        :return: Query result.
        """
        if type(query) is not StoryContextQuery:
            raise RuntimeError("Query is %s, not StoryContextQuery" % str(type(query)))
        if query.type == "sketch":
            self.apply_sketches(
                start=query.range_start,
                end=query.range_end,
                topic=str(query.content),
            )
            self.should_regenerate = True
            return None
        elif query.type == "remove_sketch":
            self.remove_sketches(
                start=query.range_start,
                end=query.range_end,
                topic=str(query.content),
            )
            self.should_regenerate = True
            return None
        elif query.type == "reset_area":
            self.reset_area(
                start=query.range_start,
                end=query.range_end,
                params=query.content,
            )
        elif query.type == "topic_weights":
            return self.get_all_topic_weights()
        elif query.type == "generate_freeze_after":
            start = query.range_start
            self.should_regenerate = True
            return self.set_freeze_mask(start)
        elif query.type == "generated_contents":
            return self.get_generated_content()
        elif query.type == "generate_one":
            return self.generate_single_sentence(
                prompt=query.content["prompt"],
                topics=query.content["topics"],
            )
        elif query.type == "force_one":
            return self.force_one_sentence(
                sentence=query.content["sentence"],
                index=query.content["index"],
            )
        elif query.type == "get_document":
            return self.document
        elif query.type == "get_all_sketches":
            return self.sketch_manager.get_all_sketches()
        elif query.type == "get_should_regenerate":
            return self.should_regenerate
        elif query.type == "reset_should_regenerate":
            self.should_regenerate = True
            return None

    def set_freeze_mask(self, start):
        """
        Set the "freeze mask" for the generation.
        After this function is called all sentence up to and including sentence [start] are set to freezed
        so that generation does not touch them anymore.
        :param start: start point (included) to set freeze.
        :return: Whether the operation is successful.
        """
        self.freeze_mask = [False] * self.sentence_count
        if start in range(self.sentence_count - 1):
            for idx in range(start + 1):
                self.freeze_mask[idx] = True
            return True
        else:
            print("Freeze mask resetted.")
            return False

    def get_generated_content(self) -> object:
        """
        Get generated sentences, using the info we already have.
        If no cache is available, we will generate fresh.
        If cache is still valid we just return the cache.
        :return: Generated sentences.
        """
        next_sentence = self.initial_prompt
        if self.should_regenerate:
            old_document = self.document
            enable_old_document = (len(old_document) == self.sentence_count)
            self.reset_document()
            self.topic_weight = self.sketch_manager.generate_weights()
            for index in range(self.sentence_count):
                # Compose topic list for each index position of the story.
                topic_this_sentence = {}
                for key, value in self.topic_weight.items():
                    topic_this_sentence[key] = value[index]

                total_weight_this_sentence = sum(topic_this_sentence.values())
                for key, value in topic_this_sentence.items():
                    if total_weight_this_sentence > 0:
                        normalized_value = value / total_weight_this_sentence
                        # Filtering weights that are too small - They do not really change the sentence but incur computation.
                        if normalized_value < 0.01 / self.sentence_count:
                            normalized_value = 0
                        topic_this_sentence[key] = normalized_value

                # Remove all keys that has weight = 0
                topic_this_sentence = {k: v for k, v in topic_this_sentence.items() if v > 0}

                # print("DEBUG: %s"%topic_this_sentence)

                # Attach one previous sentence (if we have at least two sentences) as the context (from original P&B work)
                if index >= 2:
                    prompt = "Here is a story from a story book for children. %s %s " % (
                        self.document[index - 2], self.document[index - 1])
                    # prompt = "Continue this story: %s" % (self.document[index - 1])
                elif index == 1:
                    prompt = "Here is a story from a story book for children. %s " % self.document[
                        0]  # Add the "0th" prompt back in
                else:
                    prompt = next_sentence  # Do nothing, use the last sentence / prompt.

                # If sentence is frozen masked we do not get the next sentence, instead take the one we have
                if not (enable_old_document and self.freeze_mask[index]):
                    next_sentence = call_generation_interface(prompt, topic=topic_this_sentence,
                                                              connection_profile=self.gen_api_profile)
                    self.document[index] = next_sentence
                else:
                    self.document[index] = old_document[index]
            self.should_regenerate = False
        return self.document

    def generate_single_sentence(self, prompt, topics):
        """
        Generate a single sentence based on the prompt and topic(s) supplied.
        This function does not affect the context in any way.
        :param prompt: Prompt to continue on.
        :param topics: Topic weights.
        :return: Generated sentence.
        """
        next_sentence = call_generation_interface(prompt, topic=topics, connection_profile=self.gen_api_profile)
        return next_sentence

    def reset_document(self):
        """
        Reset document so that it contains nothing.
        :return: None.
        """
        self.document = [""] * self.sentence_count

    def force_one_sentence(self, sentence, index):
        """
        Override a sentence with the given "sentence" parameter.
        :param index: Which location of the document is to override.
        :param sentence: sentence to override.
        :return: None
        """
        self.document[index] = sentence

    # region internals

    def apply_sketches(self, start: int, end: int, topic: str) -> None:
        """
        Apply a sketch to the topic weights.
        :param start: Start for this sketch.
        :param end: end for this sketch.
        :param topic: topic related to this sketch.
        :return: None.
        """
        self.should_regenerate = True
        self.sketch_manager.append(topic=topic, start=start, end=end)

    def remove_sketches(self, start: int, end: int, topic: str) -> None:
        """
        Remove a sketch to the topic weights.
        :param start: Start for this sketch.
        :param end: end for this sketch.
        :param topic: topic related to this sketch.
        :return: None.
        """
        self.should_regenerate = True
        self.sketch_manager.remove(topic=topic, start=start, end=end)

    def reset_area(self, start: int, end: int, params: object) -> None:
        """
        Reset an area to start fresh, making it free of any control parameters provided before.
        :param start: start point
        :param end: end point
        :param params: reserved.
        :return: None
        """
        print("Resetting area from %s to %s." % (start, end))
        self.should_regenerate = True
        for sketch in self.sketch_manager.get_all_sketches():
            # remove all sketches that overlaps with this area.
            s0 = sketch['start']
            s1 = sketch['end']
            if s0 > end or s1 < start:
                pass  # no change
            else:
                self.sketch_manager.remove(sketch['topic'], s0, s1)
        for i in range(start, end + 1):
            self.freeze_mask[i] = False

    def get_all_topic_weights(self):
        """
        Get all topic weights.
        :return: topic weights dictionary.
        """
        self.topic_weight = self.sketch_manager.generate_weights()
        return self.topic_weight

    def is_generated_contents_ready(self):
        """
        Can we show generated contents already?
        :return: Whether we have generated sentences ready.
        """
        return len(self.document) > 0

    def is_generation_ready(self):
        """
        Can we start generating things?
        :return: Whether we have enough information to start generating sentences.
        """
        return len(self.topic_weight) > 0

    # endregion

