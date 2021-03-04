from flask import *
from flask import Blueprint
import json

# Custom functions
from functions import *
from endpoints.graph.functions import *

graph = Blueprint('graph', __name__)

@graph.route('/find', methods=['POST', 'GET'])
def return_node():
    # Parse input parameters from request
    if request_type(request) == 'application/json':
        # parse request values from JSON
        data_json = request.json
        json_key=[*data_json][0]
        search=request.get_json()[json_key]

    else:
        raise_error("json expected")

    # if not chunk_id:
    #     raise_error("no id specified")

    nodes = find_node(search)

    if response_type(request) == "application/json":
        try:
            response = make_response(json.dumps(nodes))
            response.mimetype = 'application/json'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}
            

@graph.route('/find/chunk', methods=['POST', 'GET'])
def return_chunk():
    data_json = request.json
    json_key=[*data_json][0]
    search=request.get_json()[json_key]

    nodes = find_chunk(search)

    response = make_response(json.dumps(nodes))
    response.mimetype = 'application/json'
    return response


@graph.route('/find/chunk/<string:node_id>', methods=['POST','GET'])
def return_chunk_viaGET(node_id):
    nodes = find_chunk(node_id)

    response = make_response(json.dumps(nodes))
    response.mimetype = 'application/json'
    return response


@graph.route('/add/chunk', methods=['POST', 'GET'])
def add_chunk():
    # Parse input parameters from request
    if request_type(request) == 'application/json':
        # parse request values from JSON
        text = request.get_json()["text"]
        source_file = request.get_json()["source_file"]
        start_time = request.get_json()["start_time"]
        end_time = request.get_json()["end_time"]
        summaries  = request.get_json()["summaries"]
        entities  = request.get_json()["entities"]
        similarity  = request.get_json()["similarity"]
    else:
        raise_error("json expected")

    # if not chunk_id:
    #     raise_error("no id specified")

    chunk = add_node(text, source_file, start_time, end_time, summaries, entities, similarity)

    if response_type(request) == "application/json":
        try:
            response = make_response(json.dumps(chunk))
            response.mimetype = 'application/json'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}

    

# TODO: add missing endpoints:
# /graph/find/chunk
# /graph/find/entity
# /graph/find/summaries
# /graph/find/collection
#
# /graph/add/chunk ({chunk_id, chunk_text, etc.} (json object))
# /graph/add/summary (chunk_id, summary (json object))
# /graph/add/entity (chunk_id, entity (json object))
#
# /graph/connect/entity
# /graph/conntect/chunks
