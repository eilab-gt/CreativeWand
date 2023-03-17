import torch
from typing import List, Tuple
import numpy as np
from scipy.spatial.distance import cosine
import nltk

from .infersent import InferSent
from CreativeWand.Application.Config.CreativeContextConfig import highlighter_model_path, highlighter_w2v_path

V = 2
MODEL_PATH = highlighter_model_path % V 
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
infersent = InferSent(params_model)
infersent.load_state_dict(torch.load(MODEL_PATH))

W2V_PATH = highlighter_w2v_path
infersent.set_w2v_path(W2V_PATH)

class HighlighterInterface():
    """
    
    """


    @staticmethod
    def highlight_with_embeddings(
        sentences: List[str]
    ) -> int:
        """
        Use sentence embeddings to find the sentence most distant from the mean.
        :param sentence: list of sentences to compare.
        :return: index of most dissimilar sentence. 
        """
        infersent.build_vocab(sentences, tokenize=True)
        embeddings = infersent.encode(sentences, tokenize=True)
        mean = np.mean(embeddings, axis=0)

        max_index = -1
        max_dist = 0
        for index, embedding in enumerate(embeddings):
            dist = cosine(embedding, mean)
            if dist > max_dist:
                max_dist = dist
                max_index = index

        return max_index

    @staticmethod
    def highlight_with_entities(
        sentences: List[str]
    ) -> Tuple[int, str]:
        """
        Use nouns AND embeddings to find the sentence most distant from the mean.
        :param sentence: list of sentences to compare.
        :return: index of most standout sentence. 
        """
        # noun extraction from sentences
        nouns = []
        is_noun = lambda pos: pos[:2] == 'NN'
        for sentence in sentences:
            tokenized = nltk.word_tokenize(sentence)
            n = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
            nouns += n

        # embed nouns
        infersent.build_vocab(nouns, tokenize=True)
        embeddings = infersent.encode(nouns, tokenize=True)
        mean = np.mean(embeddings, axis=0)

        max_index = -1
        max_dist = 0
        for index, embedding in enumerate(embeddings):
            dist = cosine(embedding, mean)
            if dist > max_dist:
                max_dist = dist
                max_index = index

        # choose sentence with farthest noun
        sentence_index = -1
        word = nouns[max_index]
        for index, sentence in enumerate(sentences):
            if word in sentence:
                sentence_index = index
                break

        return sentence_index, word

