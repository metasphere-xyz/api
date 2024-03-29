## config.py

checkmark = f"[green]"u'\u2713 '
cross = f"[red]"u'\u00D7 '
eye = f"[white]"u'\u2022 '
arrow = f"[grey]"u'\u21B3 '
database = f"[white]DATABASE[/white]:"

# %% LOGGING
from rich import print
from rich import pretty
pretty.install()

print (f"[bold green]Starting up.[/bold green]")

print (eye, f"[bold]Loading [/bold]functions.")
from functions import *

print (eye, f"[bold]Loading [/bold]modules.")
# %% modules
import os
import re
import sys

# API and requests
import requests
from flask import *
import json
from http import HTTPStatus
from flask_cors import CORS, cross_origin

# calculations
import math
import hashlib
md5 = hashlib.md5()
from sklearn.metrics.pairwise import cosine_similarity
from fuzzy_match import algorithims as algorithms
from fuzzy_match import match

print (eye, f"[bold]Loading[/bold] spacy.")

# linkpreview
from linkpreview import link_preview

# nlp libraries
import spacy
# %% GENERAL NLP
text = ""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
nlp = spacy.load("en_core_web_sm")
stopwords = nlp.Defaults.stop_words

# maschine learning models and pipeplines
print (eye, f"Loading [bold]torch[/bold].")
import torch

print (eye, f"[bold]Loading[/bold] huggingface.")
from transformers import pipeline, AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer
ner_huggingface_pipeline = pipeline("ner")

print (eye, f"[bold]Loading[/bold] tensorflow.")
import tensorflow_hub as hub

# from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, T5Config


# %% DATABASE
print (eye, f"[bold]Connecting to[/bold] graph database.")
from py2neo import Graph
try:
    graph = Graph(
        "bolt://ecchr.metasphere.xyz:7687/",
        auth=('neo4j', 'burr-query-duel-cherry')
    )
except:
    print (cross, f"Can't connect to graph database. Exiting.")
    sys.exit(1)
finally:
    print (checkmark, f"Connected to graph database.")



# %% ENTITIY RECOGNITION
accepted_entity_labels = (
    'PERSON',
    'ORG',
    'GPE',
    'WORK_OF_ART',
    'NORP',
    'FAC',
    'LOC',
    'PRODUCT',
    'LAW'
)

# %% SUMMARIZATION /text/summarization

# # https://pypi.org/project/bert-extractive-summarizer/
# # useful for summarizing multiple sentences to less sentences
# from summarizer import Summarizer
# sentence_summarizer = Summarizer()

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
