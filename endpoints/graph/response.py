from flask import make_response, request
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
        "score": 0
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

def get_single_json_value():
    if request_type(request) == 'application/json':
        data_json = request.json
        json_key=[*data_json][0]
        search=request.get_json()[json_key]
        return search
    else:
        return 'json expected'

def get_chunk_json_value():
    if request_type(request) == 'application/json':
        text = request.get_json()['text']
        source_file = request.get_json()['source_file']
        start_time = request.get_json()['start_time']
        end_time = request.get_json()['end_time']
        summaries  = request.get_json()['summaries']
        entities  = request.get_json()['entities']
        similarity  = request.get_json()['similarity']
        collection_id  = request.get_json()['collection_id']
        return text, source_file, start_time, end_time, summaries, entities, similarity, collection_id
    else:
        return 'json expected'

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
        response_failed['message'] = "could not find instance (" + str(404) + ")"
        response_failed['instance']= parameters
        return response_failed
