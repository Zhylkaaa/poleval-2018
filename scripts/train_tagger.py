#!/usr/bin/env python3

"""
Trains per-group sequence tagging models, that is LSTM-CRFs with one bidirectional
LSTM layer and 512 hidden states on 300-dimensional GloVe embeddings,
as well as embeddings from forward and backward LMs with 2048 hidden states.
"""

from typing import List
from flair.embeddings import StackedEmbeddings, CharLMEmbeddings, TokenEmbeddings, FlairEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.data import Corpus

from models import FORWARD_LM, BACKWARD_LM, GLOVE
from embeddings import KeyedWordEmbeddings
from ne_groups import GROUPS
from corpora import read_group
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--embedding_storage', default='none')
    args = parser.parse_args()

    embedding_types: List[TokenEmbeddings] = [
        KeyedWordEmbeddings(GLOVE),
        FlairEmbeddings(FORWARD_LM), #CharLMEmbeddings(FORWARD_LM),
        FlairEmbeddings(BACKWARD_LM) #CharLMEmbeddings(BACKWARD_LM)
    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    for entities in GROUPS:
        corpus: Corpus = read_group(entities)
        tag_dictionary = corpus.make_tag_dictionary(tag_type='ner')
        tagger: SequenceTagger = SequenceTagger(hidden_size=512,
                                                embeddings=embeddings,
                                                tag_dictionary=tag_dictionary,
                                                tag_type='ner',
                                                use_crf=True)
        trainer: ModelTrainer = ModelTrainer(tagger, corpus)
        file_name = '-'.join(entities)
        trainer.train(f'data/models/{file_name}',
                       learning_rate=0.05,
                       mini_batch_size=124,
                       monitor_test=True,
                       embeddings_storage_mode=args.embedding_storage,
                       max_epochs=40)
