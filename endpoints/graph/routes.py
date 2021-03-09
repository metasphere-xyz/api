from flask import *
from flask import Blueprint
import json

# Custom functions
from functions import *
from endpoints.graph.database import *
from endpoints.graph.response import *

graph = Blueprint('graph', __name__)

@graph.route('/find', methods=['POST', 'GET'])
def return_node():
    search = get_single_json_value()
    # if not chunk_id:
    #     raise_error('no id specified')
    nodes = find_node(search)
    response = response_is_json(nodes)
    return response

@graph.route('/find/chunk', methods=['POST', 'GET'])
def return_chunk():
    search = get_single_json_value()
    chunk = find_chunk(search)
    response = response_is_json(chunk)
    return response

@graph.route('/find/chunk/<string:node_id>', methods=['POST','GET'])
def return_chunk_viaGET(node_id):
    chunk = find_chunk(node_id)
    response = response_is_json(chunk)
    return response

@graph.route('/find/entity', methods=['POST', 'GET'])
def return_entity():
    search = get_single_json_value()
    entity = find_entity(search)
    response = response_is_json(entity)
    return response

@graph.route('/find/entity/<string:entity_id>', methods=['POST','GET'])
def return_entity_viaGET(entity_id):
    entity = find_entity(entity_id)
    response = response_is_json(entity)
    return response

@graph.route('/find/collection', methods=['POST', 'GET'])
def return_collection():
    search = get_single_json_value()
    collection = find_collection(search)
    response = response_is_json(collection)
    return response

@graph.route('/find/collection/<string:collection_id>', methods=['POST','GET'])
def return_collection_viaGET(collection_id):
    collection = find_collection(collection_id)
    response = response_is_json(collection)
    return response

@graph.route('/find/summary', methods=['POST', 'GET'])
def return_summary():
    search = get_single_json_value()
    summary = find_summary(search)
    response = response_is_json(summary)
    return response

@graph.route('/find/summary/<string:summary_id>', methods=['POST','GET'])
def return_summary_viaGET(summary_id):
    summary = find_summary(summary_id)
    response = response_is_json(summary)
    return response

@graph.route('/add/collection', methods=['POST', 'GET'])
def add_collection():
    name, source_type, source_path, date, chunk_sequence = get_collection_json_value()

    collection = add_collection_without_connections(
        name,
        source_type,
        source_path,
        date,
        chunk_sequence
        )
    response = response_is_json(collection)
    return response

@graph.route('/add/chunk', methods=['POST', 'GET'])
def add_chunk():
    text, source_file, start_time, end_time, summaries, entities, similarity, collection_id = get_chunk_json_value()

    chunk = add_chunk_to_collection(
        text, 
        source_file, 
        start_time, 
        end_time, 
        summaries, 
        entities, 
        similarity, 
        collection_id
        )
    response = response_is_json(chunk)
    return response

@graph.route('/add/entity', methods=['POST', 'GET'])
def add_entity():
    chunk_id, name, url, entity_category = get_entity_json_value()
    print(entity_category)

    entity = add_entity_to_chunk(
        chunk_id,
        name,
        url,
        entity_category
        )
    response = response_is_json(entity)
    return response

@graph.route('/unwrap/chunk', methods=['POST', 'GET'])
def add_unwrap_chunk():
    text, source_file, start_time, end_time, summaries, entities, similarity, collection_id = get_chunk_json_value()

    unwrap_chunk = add_unwrap_chunk_to_collection(
        text, 
        source_file, 
        start_time, 
        end_time, 
        summaries, 
        entities, 
        similarity, 
        collection_id
    )

    response = response_is_json(unwrap_chunk)
    return response


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
