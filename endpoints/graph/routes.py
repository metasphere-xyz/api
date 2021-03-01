from flask import *
from flask import Blueprint
import json

# Custom functions
from functions import *
from endpoints.graph.functions import *

graph = Blueprint('graph', __name__)

@graph.route('/find', methods=['POST', 'GET'])
def return_nodes():
    # Parse input parameters from request
    if request_type(request) == 'application/json':
        # parse request values from JSON
        chunk_id = request.get_json()["chunk_id"]
    else:
        raise_error("json expected")

    if not chunk_id:
        raise_error("no id specified")

    # calculate response via summarize function
    nodes = find_node(chunk_id)

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
