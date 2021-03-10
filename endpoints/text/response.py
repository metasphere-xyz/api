
def response_is_json(text_return):
    if response_type(request) == 'application/json':
        try:
            response = make_response(json.dumps(text_return))
            response.mimetype = 'application/json'
            return response
        except Exception as ex:
            traceback.print_exc()
            return {'status': 'failed', 'error': str(ex)}
    else:
        return 'error'