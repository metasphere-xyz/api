from flask import *
from flask import Blueprint
import json

# Custom functions
from functions import *
from endpoints.text.functions import *
from endpoints.text.text_processing import *
from endpoints.text.request import *
from endpoints.text.response import *


text = Blueprint('text', __name__)

@text.route('/extract/entities', methods=['POST', 'GET'])
def return_ner():
    text = get_text_json()
    ner_output = ner(text)
    response = response_is_json(ner_output)
    return response

@text.route('/similarity', methods=['POST', 'GET'])
def return_similarities():
    text, similarities = get_chunk_json()
    similarity = similarity_tf(text, similarities)
    response = response_is_json(similarity)
    return response

@text.route('/summarize', methods=['POST', 'GET'])
def return_summaries():
    # Parse input parameters from request
    if request_type(request) == 'text/plain':
        text = request
    elif request_type(request) == 'application/json':
        # parse request values from JSON
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

# TODO: add missing endpoints:
# /text/extract/chunks
# /text/extract/entities
# /text/find/similar -- working title

    #
    #
    # if request.content_type == app_json and accept_json==1:
    #
    #     data = {
    #             "chunk_id": "md5sum",
    #             "summary": [
    #             ]
    #         }
    #
    #     if request.is_json:
    #         req_json = request.get_json()
    #
    #         text = req_json["text"]
    #         aim = req_json["aim"]
    #         deviation = req_json["deviation"]
    #         num_summaries = req_json["num_summaries"]
    #
    #         text_chunk = [""] * num_summaries
    #         compression = [0] * num_summaries
    #         aim_rel = [0] * num_summaries
    #         deviation_output = [0] * num_summaries
    #
    #         # Generate n>1 summaries by multiple summary call -> no num_summaries case distinction
    #         text_chunk, compression, aim_rel, deviation_output = summary(text, aim=aim, deviation_input=deviation, num_summaries=num_summaries)
    #
    #         if num_summaries>1:
    #             for i in range(num_summaries):
    #                 data["summary"].append(
    #                     {
    #                         "text": text_chunk[i],
    #                         "summary_id": i,
    #                         "compression": compression[i],
    #                         "aim": aim_rel[i],
    #                         "deviation": deviation_output[i]
    #                     },
    #                 )
    #         else:
    #             data["summary"].append(
    #                     {
    #                         "text": text_chunk,
    #                         "summary_id": 1,
    #                         "compression": compression,
    #                         "aim": aim_rel,
    #                         "deviation": deviation_output
    #                     },
    #                 )
    #
    #         data_json = json.dumps(data)
    #         response = make_response(data_json)
    #         response.mimetype=app_json
    #
    #         return response
    #
    # # # HTML -> MTML
    # # if request.content_type == html and accept_html==1:
    #
    # #     response = Response(summary, mimetype=html)
    #
    # # # TEXT/PLAIN -> TEXT/PLAIN
    # # if request.content_type == text and accept_text==1:
    #
    # #     response = Response(summary, mimetype=text)
    #
    # # # TEXT/PLAIN -> APPLICATION/JSON
    # # if request.content_type == text and accept_text==1:
    #
    # #     response = Response(summary, mimetype=json)
    #
    # # # JSON -> TEXT/PLAIN
    # # if request.content_type == text and accept_text==1:
    #
    # #     response = Response(summary, mimetype=text)
    #
    # return "endpoint: summary"
