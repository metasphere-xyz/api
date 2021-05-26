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
        elif endpoint == 'summarize_chunk_sequence':
            chunk_sequence = []
            try:
                chunk_sequence = request.get_json()['chunk_sequence']
            except Exception as ex:
                raise_error("no chunk sequence specified")

            if len(chunk_sequence) < 1:
                raise_error("no chunk sequence specified")
            return chunk_sequence

def parse_json_from_request():
    if request_type(request) == 'application/json':
        try:
            # make sure we get json in the first place
            request_json = request.get_json()
        except:
            return 'could not unpack json'
        finally:
            values_from_json = json.loads(str(json.dumps(request_json)))
            return values_from_json
    else:
        return 'json expected'