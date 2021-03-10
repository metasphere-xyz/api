from flask import *
from flask import Blueprint
import json

# Custom functions
from config import *
from functions import *
from endpoints.text.functions import *
from endpoints.text.text_processing import *
from endpoints.text.request import *
from endpoints.text.response import *

text = Blueprint('text', __name__)

@text.route('/extract/entities', methods=['POST', 'GET'])
def return_ner():
    text = parse_json('text')
    ner_output = ner(text)
    response = response_is_json(ner_output)
    return response

@text.route('/similarity', methods=['POST', 'GET'])
def return_similarities():
    text, num_similar_chunks = parse_json('similarity')
    similar_chunks = similarity_tf(text, num_similar_chunks)
    response = response_is_json(similar_chunks)
    return response

@text.route('/summarize', methods=['POST', 'GET'])
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
