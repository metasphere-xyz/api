from config import *

<<<<<<< HEAD
def respond_with_json(payload):
    try:
        response = make_response(json.dumps(payload))
        response.mimetype = 'application/json'
        return response
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}
=======
# def respond_with_json(payload):
#     try:
#         response = make_response(json.dumps(payload))
#         response.mimetype = 'application/json'
#         return response
#     except Exception as ex:
#         traceback.print_exc()
#         return {'status': 'failed', 'error': str(ex)}
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
