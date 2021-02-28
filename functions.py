# Helper functions for dealing with requests:

# response_type(request):
# returns accepted response type as String
def response_type(request):
    accepted_response_types = (
        'application/json',
        'text/plain',
        'text/html'
    )

    # filter for accepted response types:
    for accepted_response in accepted_response_types:
        if request.accept_mimetypes[accepted_response] == 1:
            # return response type
            return accepted_response
        else:
            return "unsupported response type"

# request_type(request):
# returns accepted request type as String
def request_type(request):
    accepted_request_types = (
        'application/json',
        'text/plain',
        'text/html'
    )

    # filter for accepted request types:
    if request.content_type in accepted_request_types:
        return request.content_type
    else:
        return "unsupported request type"