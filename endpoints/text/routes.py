from flask import *
from flask import Blueprint
from endpoints.text.functions import *
from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")
import json

text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    json = 'application/json'
    text = 'text/plain'
    accept_json = request.accept_mimetypes['application/json']
    accept_text = request.accept_mimetypes['application/json']


    if request.content_type == json and accept_json==1:
        print('application/json')
        if request.is_json:
            text = request.json.get("text")
            aim = request.json.get("aim")
            summary_content = summarizer(str(text), min_length=5, max_length=10)
            summary = str(summary_content)

            # response = app.response_class(
            #     response=json.dumps(summary),
            #     status=200,
            #     mimetype='application/json'
            # ) 
            # -> not working out of the box -> customizing of the flask response class necessary

            response = Response(summary, mimetype='application/json')

            return response

    return "test"
