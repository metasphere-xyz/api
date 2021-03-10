from config import *

def parse_json(endpoint):
    if request_type(request) != 'application/json':
        return 'json expected'
    else:
        if endpoint == 'similarity':
            text = request.get_json()['text']
            num_chunks = request.get_json()['chunks']
            if int(request.get_json()['minimum_score']) > 0:
                similarity_score_treshold = str(request.get_json()['minimum_score'])
            # define standard values
            if not text:
                raise_error("no text specified")
            return text, num_chunks, similarity_score_treshold
        elif endpoint == 'text':
            if not request.get_json()['text']:
                raise_error("no text specified")
            return request.get_json()['text']
        elif endpoint == 'summarize':
            text = request.get_json()["text"]
            aim = request.get_json()["aim"]
            deviation = request.get_json()["deviation"]
            num_summaries = request.get_json()["num_summaries"]
            # define standard values
            if not text:
                raise_error("no text specified")
            return text, aim, deviation, num_summaries