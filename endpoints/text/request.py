from flask import make_response, request
import traceback
import json
from functions import *

def get_text_json():
    if request_type(request) == 'application/json':
        text = request.get_json()['text']
        return text
    else:
        return 'json expected'