# Custom functions
from endpoints.graph.database import *
from endpoints.graph.response import *
from endpoints.graph.request import *

from flask import Blueprint
graph_routes = Blueprint('graph', __name__)

@graph_routes.route('/find', methods=['POST', 'GET'])
def return_node():
    search = get_single_json_value()
    # if not chunk_id:
    #     raise_error('no id specified')
    nodes = find_node(search)
    response = response_is_json(nodes)
    return response

@graph_routes.route('/find/chunk', methods=['POST', 'GET'])
def return_chunk():
    search = get_single_json_value()
    chunk = find_chunk(search)
    response = response_is_json(chunk)
    return response

@graph_routes.route('/find/chunk/<string:node_id>', methods=['POST','GET'])
def return_chunk_viaGET(node_id):
    chunk = find_chunk(node_id)
    response = response_is_json(chunk)
    return response

@graph_routes.route('/find/entity', methods=['POST', 'GET'])
def return_entity():
    search = get_single_json_value()
    entity = find_entity(search)
    response = response_is_json(entity)
    return response

@graph_routes.route('/find/entity/<string:entity_id>', methods=['POST','GET'])
def return_entity_viaGET(entity_id):
    entity = find_entity(entity_id)
    response = response_is_json(entity)
    return response

@graph_routes.route('/find/collection', methods=['POST', 'GET'])
def return_collection():
    search = get_single_json_value()
    collection = find_collection(search)
    response = response_is_json(collection)
    return response

@graph_routes.route('/find/collection/<string:collection_id>', methods=['POST','GET'])
def return_collection_viaGET(collection_id):
    collection = find_collection(collection_id)
    response = response_is_json(collection)
    return response

@graph_routes.route('/find/summary', methods=['POST', 'GET'])
def return_summary():
    search = get_single_json_value()
    summary = find_summary(search)
    response = response_is_json(summary)
    return response

@graph_routes.route('/find/summary/<string:summary_id>', methods=['POST','GET'])
def return_summary_viaGET(summary_id):
    summary = find_summary(summary_id)
    response = response_is_json(summary)
    return response

@graph_routes.route('/add/collection', methods=['POST', 'GET'])
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

@graph_routes.route('/add/chunk', methods=['POST', 'GET'])
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

@graph_routes.route('/add/entity', methods=['POST', 'GET'])
def add_entity():
    chunk_id, name, url, entity_category = get_entity_json_value()

    entity = add_entity_to_chunk(
        chunk_id,
        name,
        url,
        entity_category
        )
    response = response_is_json(entity)
    return response

@graph_routes.route('/add/summary', methods=['POST', 'GET'])
def add_summary():
    chunk_id, summary_id, text, compression, aim, deviation = get_summary_json_value()

    summary = add_summary_to_chunk(
        chunk_id,
        summary_id,
        text,
        compression,
        aim,
        deviation
        )
    response = response_is_json(summary)
    return response

@graph_routes.route('/unwrap/chunk', methods=['POST', 'GET'])
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

@graph_routes.route('/connect/chunk', methods=['POST', 'GET'])
def connect_chunk():
    connect, with_id, with_score = connect_chunk_json_value()

    connected_nodes = connect_chunk_to_chunk(
        connect,
        with_id,
        with_score
    )
    response = response_is_json(connected_nodes)
    return response

@graph_routes.route('/connect/entity', methods=['POST', 'GET'])
def connect_entity():
    connect, with_id = connect_entity_json_value()

    connected_nodes = connect_entity_to_chunk(
        connect,
        with_id
    )
    response = response_is_json(connected_nodes)
    return response

@graph_routes.route('/disconnect/chunk', methods=['POST', 'GET'])
def disconnect_chunk():
    disconnect, from_id = disconnect_entity_json_value()

    disconnected_nodes = disconnect_chunk_from_chunk(
        disconnect,
        from_id
        )
    response = response_is_json(disconnected_nodes)
    return response

@graph_routes.route('/disconnect/entity', methods=['POST', 'GET'])
def disconnect_entity():
    disconnect, from_id = disconnect_entity_json_value()

    disconnected_nodes = disconnect_entity_from_chunk(
        disconnect,
        from_id
        )
    response = response_is_json(disconnected_nodes)
    return response


# TODO: add missing endpoints:
#
# /graph/add/chunk ({chunk_id, chunk_text, etc.} (json object))
# /graph/add/summary (chunk_id, summary (json object))
# /graph/add/entity (chunk_id, entity (json object))
#
# /graph/connect/entity
# /graph/conntect/chunks
