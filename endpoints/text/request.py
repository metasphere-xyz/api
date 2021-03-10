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
