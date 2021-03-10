from config import *
import json
import traceback
from flask import make_response

# Accepted Request content types
accepted_request_types = (
    'application/json',
    'text/plain',
    'text/html'
)

# Accepted Response accept_mimetypes
accepted_response_types = (
    'application/json',
    'text/plain',
    'text/html'
)

def respond_with_json(payload):
    try:
        response = make_response(json.dumps(payload))
        response.mimetype = 'application/json'
        return response
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}


def response_type(request):
    # filter for accepted response types:
    for accepted_response in accepted_response_types:
        if request.accept_mimetypes[accepted_response] == 1:
            # return response type
            return accepted_response
        else:
            return raise_error("unsupported response type", request)


def request_type(request):
    # filter for accepted request types:
    if request.content_type in accepted_request_types:
        # make sure JSON is valid
        if request.content_type == 'application/json':
            if not request.is_json:
                return raise_error("malformed json", request)
        return request.content_type
    else:
        return raise_error("unsupported request type", request)

# Error handling
def raise_error(error_type, request=""):
    def return_formatted(message):
        # TODO/Backlog: reformat into JSON outputs
        return str(message)

    if error_type == "unsupported response type":
        message = "Error: Unsupported Accept-Response Type. Supported are: " + ', '.join(accepted_response_types)

    if error_type == "unsupported request type":
        message = "Error: Unsupported Request Content-Type (" + request.content_type + "). Supported are: " + ', '.join(accepted_request_types)

    if error_type == "malformed json":
        message = "Error: Malformed JSON"

    if error_type == "no text specified":
        message = "Error: No input text specified"

    if error_type == "no id specified":
        message = "Error: No id specified"

    if error_type == "json expected":
        message = "Error: Unexpected Request Content-Type (" + request.content_type + "). Expected Content-Type is application/json"

    return return_formatted(message)
