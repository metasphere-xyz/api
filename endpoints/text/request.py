from flask import make_response, request
import traceback
import json
from functions import *

def get_text_json():
    if request_type(request) == 'application/json':
        text = request.get_json()['text']
        return text
    else:
        return 'json expected'

def parse_json_similarity():
    if request_type(request) == 'application/json':
        text = request.get_json()['text']
        num_chunks = request.get_json()['chunks']
        if not num_chunks:
            num_chunks = 3
        return text, num_chunks
    else:
        return 'json expected'

def parse_json(endpoint):
    if request_type(request) != 'application/json':
        return 'json expected'
    else:
        if endpoint == 'similarity':
            text = request.get_json()['text']
            num_chunks = request.get_json()['chunks']
            # define standard values
            if not num_chunks:
                num_chunks = 3
            return text, num_chunks
        elif endpoint == 'text':
            text = request.get_json()['text']
            return text
        elif endpoint == 'summarize':
            text = request.get_json()["text"]
            aim = request.get_json()["aim"]
            deviation = request.get_json()["deviation"]
            num_summaries = request.get_json()["num_summaries"]
            # define standard values
            if not text:
                raise_error("no text specified")
            if not aim:
                aim = "50"
            if not deviation:
                deviation = "10"
            if not num_summaries:
                num_summaries = "1"
            return text, aim, deviation, num_summaries