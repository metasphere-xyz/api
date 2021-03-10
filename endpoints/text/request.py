from config import *

def parse_json(endpoint):
    if request_type(request) != 'application/json':
        return 'json expected'
    else:
        if endpoint == 'similarity':
            text = request.get_json()['text']
            num_chunks = request.get_json()['chunks']
            # define standard values
            if not text:
                raise_error("no text specified")
            return text, num_chunks
        elif endpoint == 'text':
            text = request.get_json()['text']
            if not text:
                raise_error("no text specified")
            return text
        elif endpoint == 'summarize':
            text = request.get_json()["text"]
            aim = request.get_json()["aim"]
            deviation = request.get_json()["deviation"]
            num_summaries = request.get_json()["num_summaries"]
            # define standard values
            if not text:
                raise_error("no text specified")
            return text, aim, deviation, num_summaries