## config.py

from functions import *

# %% modules
import os

# API and requests
from flask import *
import json
from http import HTTPStatus

# calculations
import math
import hashlib
md5 = hashlib.md5()
from sklearn.metrics.pairwise import cosine_similarity
from fuzzy_match import algorithims as algorithms

# nlp libraries
import spacy

# maschine learning models and pipeplines
import torch
from transformers import pipeline, AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow_hub as hub

# from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, T5Config


# %% DATABASE
from py2neo import Graph
graph = Graph(
    "bolt://ecchr.metasphere.xyz:7687/",
    auth=('neo4j', 'burr-query-duel-cherry')
)



# %% GENERAL NLP
text = ""
nlp = spacy.load("en_core_web_sm")
ner_huggingface_pipeline = pipeline("ner")

# %% ENTITIY RECOGNITION
accepted_entity_labels = (
    'PERSON',
    'ORG',
    'DATE',
    'GPE'
)

# %% SUMMARIZATION /text/summarization

# # https://pypi.org/project/bert-extractive-summarizer/
# # useful for summarizing multiple sentences to less sentences
# from summarizer import Summarizer
# sentences_summarizes = Summarizer()

aim = "50"
deviation = "10"
num_summaries = "3"
summary_percentage_document = "10"
chunk_sequence = []

# summarization_model = "facebook/bart-base"
# summarization_model = "facebook/bart-large-cnn"
summarization_model = "t5-small"
# summarization_model = "t5-base"
# summarization_model = "t5-large"
# summarization_model = "gpt2"
summarization_model_parameters = {
    # input_ids[torch.LongTensor],
    "do_sample": False,
    "early_stopping": True,
    # "early_stopping": False,
    "num_beams": 5,
    "temperature": 1.0,
    "top_k": 50,
    "top_p": 1.0,
    "repetition_penalty": 1.5,
    # pad_token_id[int],
    # bos_token_id[int],
    # eos_token_id[int],
    "length_penalty": 5.0,
    "no_repeat_ngram_size": 3,
    # bad_words_ids=List[List[int]],
    "num_return_sequences": 1,
    # attention_mask=(batch_size, sequence_length),
    # decoder_start_token_id[int],
    "use_cache": True,
    # prefix_allowed_tokens_fn(Callable[[int, torch.Tensor], List[int]]),
    # model_kwargs
}


# %% SIMILARITY /text/similarities
num_similar_chunks = "3"
default_edge_weigth = "50"
similarity_score_treshold = "80"
