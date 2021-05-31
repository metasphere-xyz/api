from config import *

def respond_with_json(payload):
    try:
        response = make_response(json.dumps(payload))
        response.mimetype = 'application/json'
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}
