# Custom functions
from config import *
from functions import *

from endpoints.graph.database import *
from endpoints.graph.response import *
from endpoints.graph.request import *
from endpoints.graph.helper import *

from flask import Blueprint
graph_routes = Blueprint('graph', __name__)

@graph_routes.route('/find', methods=['POST', 'GET'])
def return_node():
    search = get_single_json_value()
    # if not chunk_id:
    #     raise_error('no id specified')
    nodes = find_node(search)
    response = respond_with_json(nodes)
    return response

@graph_routes.route('/find/chunk', methods=['POST', 'GET'])
def return_chunk():
    search = get_single_json_value()
    chunk = find_chunk(search)
    response = respond_with_json(chunk)
    return response

@graph_routes.route('/find/chunk/<string:node_id>', methods=['POST','GET'])
def return_chunk_viaGET(node_id):
    chunk = find_chunk(node_id)
    response = respond_with_json(chunk)
    return response

@graph_routes.route('/find/entity', methods=['POST', 'GET'])
def return_entity():
    search = get_single_json_value()
    entity = find_entity(search)
    response = respond_with_json(entity)
    return response

@graph_routes.route('/find/entity/<string:entity_id>', methods=['POST','GET'])
def return_entity_viaGET(entity_id):
    entity = find_entity(entity_id)
    response = respond_with_json(entity)
    return response

@graph_routes.route('/find/collection', methods=['POST', 'GET'])
def return_collection():
    search = get_single_json_value()
    collection = find_collection(search)
    response = respond_with_json(collection)
    return response

@graph_routes.route('/find/collection/<string:collection_id>', methods=['POST','GET'])
def return_collection_viaGET(collection_id):
    collection = find_collection(collection_id)
    response = respond_with_json(collection)
    return response

@graph_routes.route('/find/summary', methods=['POST', 'GET'])
def return_summary():
    search = get_single_json_value()
    summary = find_summary(search)
    response = respond_with_json(summary)
    return response

@graph_routes.route('/find/summary/<string:summary_id>', methods=['POST','GET'])
def return_summary_viaGET(summary_id):
    summary = find_summary(summary_id)
    response = respond_with_json(summary)
    return response

@graph_routes.route('/add/collection', methods=['POST', 'GET'])
def add_collection():
    name, source_type, source_path, date, chunk_sequence = get_collection_json_value()

    collection_with_chunks = add_collection_with_chunks(
        name,
        source_type,
        source_path,
        date,
        chunk_sequence
        )
    response = respond_with_json(collection_with_chunks)
    return response

@graph_routes.route('/add/collection-without-chunks', methods=['POST', 'GET'])
def add_collection_no_chunks():
    name, source_type, source_path, date, chunk_sequence = get_collection_json_value()

    collection = add_collection_without_chunks(
        name,
        source_type,
        source_path,
        date,
        chunk_sequence
        )
    response = respond_with_json(collection)
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
    response = respond_with_json(chunk)
    return response

@graph_routes.route('/add/entity', methods=['POST', 'GET'])
def add_entity():
    chunk_id, name, url, entity_label = get_entity_json_value()

    entity = add_entity_to_chunk(
        chunk_id,
        name,
        url,
        entity_label
        )
    response = respond_with_json(entity)
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
    response = respond_with_json(summary)
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
    response = respond_with_json(unwrap_chunk)
    return response

@graph_routes.route('/update/chunk', methods=['POST', 'GET'])
def update_chunk():
    chunk_id, text, source_file, start_time, end_time, summaries, entities, similarity, collection_id = update_chunk_json_value()

    # optionalParameter(chunk_id, source_file, start_time, end_time, summaries, entities, similarity)

    response = find_chunk(chunk_id)
    if response["status"]=="success":
        print("chunk was found")
        if source_file != None:
            source_file = source_file
        else:
            source_file = response["instance"]["source_file"]

        if start_time != None:
            start_time = start_time
        else:
            start_time = response["instance"]["start_time"]

        if end_time != None:
            end_time = end_time
        else:
            end_time = response["instance"]["end_time"]

        if summaries != None:
            summaries = summaries
        else:
            summaries = response["instance"]["summaries"]

        if entities != None:
            entities = entities
        else:
            entities = response["instance"]["entities"]
        
        if similarity != None:
            similarity = similarity
        else:
            similarity = response["instance"]["similarity"]
        
        updated_chunk = update_chunk_data(
        chunk_id, 
        text,
        source_file, 
        start_time, 
        end_time, 
        summaries, 
        entities, 
        similarity, 
        collection_id
    )
    else:
        print("chunk does not exist")  
    
    response = respond_with_json(updated_chunk)  
    return response


@graph_routes.route('/connect/chunk', methods=['POST', 'GET'])
def connect_chunk():
    connect, with_id, with_score = connect_chunk_json_value()

    connected_nodes = connect_chunk_to_chunk(
        connect,
        with_id,
        with_score
    )
    response = respond_with_json(connected_nodes)
    return response

@graph_routes.route('/connect/entity', methods=['POST', 'GET'])
def connect_entity():
    connect, with_id = connect_entity_json_value()

    connected_nodes = connect_entity_to_chunk(
        connect,
        with_id
    )
    response = respond_with_json(connected_nodes)
    return response

@graph_routes.route('/disconnect/chunk', methods=['POST', 'GET'])
def disconnect_chunk():
    disconnect, from_id = disconnect_entity_json_value()

    disconnected_nodes = disconnect_chunk_from_chunk(
        disconnect,
        from_id
        )
    response = respond_with_json(disconnected_nodes)
    return response

@graph_routes.route('/disconnect/entity', methods=['POST', 'GET'])
def disconnect_entity():
    disconnect, from_id = disconnect_entity_json_value()

    disconnected_nodes = disconnect_entity_from_chunk(
        disconnect,
        from_id
        )
    response = respond_with_json(disconnected_nodes)
    return response


# TODO: add missing endpoints:
#
# /graph/add/chunk ({chunk_id, chunk_text, etc.} (json object))
# /graph/add/summary (chunk_id, summary (json object))
# /graph/add/entity (chunk_id, entity (json object))
#
# /graph/connect/entity
# /graph/conntect/chunks
