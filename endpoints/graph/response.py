from flask import make_response, request
import traceback
import json
from functions import *
from http import HTTPStatus
from py2neo import Graph

graph = Graph(
    "bolt://ecchr.metasphere.xyz:7687/",
    auth=('neo4j', 'burr-query-duel-cherry')
)

response_success = {
    "status": "success",
}

response_failed = {
    "status": "failed",
}

response_connect = {
    "status": "success",
    "connected": {},
    "with": {
        "node": {

        },
        "score": 50
    }
}

response_disconnect = {
    "status": "success",
    "disconnected": {},
    "from": {
        "node": {

        },
        "relation": ""
    }
}

def response_is_json(graph_return):
    if response_type(request) == 'application/json':
        try:
            response = make_response(json.dumps(graph_return))
            response.mimetype = 'application/json'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}
    else:
        return 'error'
 
def submit(query, parameters):
    try:
        result = graph.run(query, parameters).data()
        result=result[0]['db_return']
        response_success['instance']=result
        return response_success
    except:
        traceback.print_exc()
        response_failed['message'] = "could not find instance (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed

def connect_chunk_to_chunk_submit(query, parameters):
    try:
        result = graph.run(query, parameters).data()
        start_chunk = result[0]['n1']
        end_chunk = result[0]['n2']
        similarity = result[0]['similarity']
        response_connect['connected'] = start_chunk
        response_connect['with']['node'] = end_chunk
        response_connect['with']['score'] = similarity
        return response_connect
    except:
        traceback.print_exc()
        response_failed['message'] = "could not create connection (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed

def connect_entity_to_chunk_submit(query, parameters):
    try:
        result = graph.run(query, parameters).data()
        entity = result[0]['e']
        chunk = result[0]['c']
        response_connect['connected'] = entity
        response_connect['with']['node'] = chunk
        return response_connect
    except:
        traceback.print_exc()
        response_failed['message'] = "could not create connection (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed

def disconnect_chunk_from_chunk_submit(query, parameters):
    try:
        result = graph.run(query, parameters).data()
        chunk = result[0]['c']
        collection = result[0]['co']
        response_disconnect['disconnected'] = chunk
        response_disconnect['from']['node'] = collection
        return response_disconnect
    except:
        traceback.print_exc()
        response_failed['message'] = "could not create connection (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed

def disconnect_entity_from_chunk_submit(query, parameters):
    try:
        result = graph.run(query, parameters).data()
        entity = result[0]['e']
        chunk = result[0]['c']
        response_disconnect['disconnected'] = entity
        response_disconnect['from']['node'] = chunk
        return response_disconnect
    except:
        traceback.print_exc()
        response_failed['message'] = "could not create connection (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed
