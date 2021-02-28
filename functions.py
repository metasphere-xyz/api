# Helper functions
import hashlib
hash = hashlib.md5()
import json

# Helper functions for dealing with requests:

# response_type(request):
# returns accepted response type as String
accepted_response_types = (
    'application/json',
    'text/plain',
    'text/html'
)

def response_type(request):
    # filter for accepted response types:
    for accepted_response in accepted_response_types:
        if request.accept_mimetypes[accepted_response] == 1:
            # return response type
            return accepted_response
        else:
            return raise_error("unsupported response type", request)

# request_type(request):
# returns accepted request type as String
accepted_request_types = (
    'application/json',
    'text/plain',
    'text/html'
)

def request_type(request):
    # filter for accepted request types:
    if request.content_type in accepted_request_types:
        # make sure JSON is valid
        request.content_type == 'application/json':
            if !request.is_json:
                return raise_error("malformed json", request)
        return request.content_type
    else:
        return raise_error("unsupported request type", request)

# Error handling
# TODO/Backlog: reformat into JSON outputs
def raise_error(error_type, request=""):
    def return_formatted(message):
        return str(message)

    if error_type == "unsupported response type":
        message = "Error: Unsupported Accept-Response Type. Supported are: " + ', '.join(accepted_response_types)

    if error_type == "unsupported request type":
        message = "Error: Unsupported Request Content-Type (" + request.content_type + "). Supported are: " + ', '.join(accepted_request_types)

    if error_type == "malformed json":
        message = "Error: Malformed JSON"

    if error_type == "no text specified":
        message = "Error: No input text specified"

    return return_formatted(message)
