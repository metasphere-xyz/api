from config import *
from flask import make_response

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
        "score": default_edge_weigth
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

# def response_is_json(graph_return):
#     if response_type(request) == 'application/json':
#         try:
#             response = make_response(json.dumps(graph_return))
#             response.mimetype = 'application/json'
#             return response
#         except Exception as ex:
#             traceback.print_exc()
#             return {'status': 'failed', 'error': str(ex)}
#     else:
#         return 'error'

def submit(query, parameters):
    try:
        print (f"{query}\n")
        print (f"{parameters}\n")
        result = graph.run(query, parameters).data()
        if result:
            db_return = result[0]['db_return']
            response_success['instance'] = db_return
            print (f"[green]found instance: {db_return}[/green]")
            return response_success
        else:
            response_failed['message'] = "instance not found"
            response_failed['instance'] = parameters
            print (f"[red]{response_failed['message']}[/red]")
            return response_failed
    except:
        traceback.print_exc()
        response_failed['message'] = "neo4j query failed"
        response_failed['instance'] = parameters
        print (f"[red]{response_failed['message']}[/red]")
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

