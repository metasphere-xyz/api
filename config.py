## config.py

# %% modules
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

import math
import hashlib
md5 = hashlib.md5()

import torch
from transformers import pipeline
# from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from transformers import AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer

import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

from fuzzy_match import algorithims as algorithms
import spacy


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

# %% SUMMARIZATION /text/summarization

# # https://pypi.org/project/bert-extractive-summarizer/
# # useful for summarizing multiple sentences to less sentences
# from summarizer import Summarizer
# sentences_summarizes = Summarizer()

aim = "50"
deviation = "10"
num_summaries = "1"

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
model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
# model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")
# model = hub.load("models/universal-sentence-encoder_4")

