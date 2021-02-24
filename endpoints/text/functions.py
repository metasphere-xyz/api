from flask import Flask, request, Response, jsonify

def return_accepted_requests(response):
    if request.accept_mimetypes["plain/text"]==1:
        return Response(response, mimetype='text/plain')
    if request.accept_mimetypes["application/json"]==1:
        if not response.is_json:
            response = jsonify(response)
        return Response(response, mimetype='application/json')