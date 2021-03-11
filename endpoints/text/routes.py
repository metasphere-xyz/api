# Custom functions
from config import *

from endpoints.text.functions import *
from endpoints.text.request import *
from endpoints.text.response import *

from flask import Blueprint
text_routes = Blueprint('text', __name__)

@text_routes.route('/extract/entities', methods=['POST', 'GET'])
def return_ner():
    text = parse_json('text')
    ner_output = ner(text)
    response = respond_with_json(ner_output)
    return response

@text_routes.route('/similarities', methods=['POST', 'GET'])
def return_similarities():
    text, num_similar_chunks, similarity_score_treshold = parse_json('similarity')
    # similar_chunks = similarity_tf(text, num_similar_chunks, similarity_score_treshold)
    similar_chunks = similarity_huggingface(text, num_similar_chunks, similarity_score_treshold)
    response = respond_with_json(similar_chunks)
    return response

@text_routes.route('/summarize', methods=['POST', 'GET'])
def return_summaries():
    if request_type(request) == 'text/plain':
        text = request
    elif request_type(request) == 'application/json':
        (text, aim, deviation, num_summaries) = parse_json('summarize')

    # calculate response via summarize function
    summary = summarize(
        text,
        aim,
        deviation,
        num_summaries,
        response_type
    )

# TODO: wrap request generation into function to get rid of repeating code
# TODO: bugfixing

    if response_type(request) == "text/plain":
        try:
            response = make_response(summary["summary"][0])
            response.mimetype = 'text/plain'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}

    elif response_type(request) == "application/json":
        try:
            response = make_response(json.dumps(summary))
            response.mimetype = 'application/json'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}
