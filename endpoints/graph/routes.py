from flask import *
from flask import Blueprint
import json

# Custom functions
from functions import *
from endpoints.graph.cypher import *
from endpoints.graph.response import *

graph = Blueprint('graph', __name__)

@graph.route('/find', methods=['POST', 'GET'])
def return_node():
    # Parse input parameters from request
    if request_type(request) == 'application/json':
        search = get_single_json_value()
    else:
        raise_error('json expected')

    # if not chunk_id:
    #     raise_error('no id specified')

    nodes = find_node(search)

    if response_type(request) == 'application/json':
        try:
            return response_json(nodes)
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}


@graph.route('/find/chunk', methods=['POST', 'GET'])
def return_chunk():
    if request_type(request) == 'application/json':
        search = get_single_json_value()

    chunk = find_chunk(search)
    return response_is_json(chunk)


@graph.route('/find/chunk/<string:node_id>', methods=['POST','GET'])
def return_chunk_viaGET(node_id):
    chunk = find_chunk(node_id)
    return response_is_json(chunk)


@graph.route('/find/entity', methods=['POST', 'GET'])
def return_entity():
    search = get_single_json_value()
    entity = find_entity(search)
    return response_is_json(entity)

@graph.route('/find/entity/<string:entity_id>', methods=['POST','GET'])
def return_entity_viaGET(entity_id):
    nodes = find_entity(entity_id)
    return response_is_json(nodes)


@graph.route('/add/chunk', methods=['POST', 'GET'])
def add_chunk():
    # Parse input parameters from request
    if request_type(request) == 'application/json':
        # parse request values from JSON
        text = request.get_json()['text']
        source_file = request.get_json()['source_file']
        start_time = request.get_json()['start_time']
        end_time = request.get_json()['end_time']
        summaries  = request.get_json()['summaries']
        entities  = request.get_json()['entities']
        similarity  = request.get_json()['similarity']
    else:
        raise_error('json expected')

    # if not chunk_id:
    #     raise_error('no id specified')

    chunk = add_node(text, source_file, start_time, end_time, summaries, entities, similarity)

    if response_type(request) == 'application/json':
        try:
            return response_json(chunk)
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}


@graph.route('/unwrap/chunk', methods=['POST', 'GET'])
def add_unwrap_chunk():
    if request_type(request) == 'application/json':
        # parse request values from JSON
        text = request.get_json()['text']
        source_file = request.get_json()['source_file']
    else:
        raise_error('json expected')

    unwrap_chunk = add_unwrap_node(text, source_file)

    if response_type(request) == 'application/json':
        try:
            return response_json(unwrap_chunk)
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}


@graph.route('/connect/chunk', methods=['POST', 'GET'])
def connect_chunk():
    if request_type(request) == 'application/json':
        # parse request values from JSON
        connect = request.get_json()['connect']
        with_id = request.get_json()['with']['id']
        with_score = request.get_json()['with']['score']
        
    else:
        raise_error('json expected')
    
    connected_nodes = connect_nodes(connect, with_id, with_score)

    if response_type(request) == 'application/json':
        try:
            return response_json(connected_nodes)
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}


@graph.route('/disconnect/chunk', methods=['POST', 'GET'])
def disconnect_chunk():
    if request_type(request) == 'application/json':
        # parse request values from JSON
        disconnect = request.get_json()['disconnect']
        from_id = request.get_json()['from']['id']
        from_relation = request.get_json()['from']['relation']
        
    else:
        raise_error('json expected')
    
    disconnected_nodes = disconnect_nodes(disconnect, from_id, from_relation)

    if response_type(request) == 'application/json':
        try:
            return response_json(disconnected_nodes)
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
