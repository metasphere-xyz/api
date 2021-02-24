from flask import *
from flask import Blueprint
from endpoints.text.functions import *
from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")


text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    if request.content_type == 'text/plain':
        print('text/plain')
        text = request.data
    if request.content_type == 'application/json':
        print('application/json')
        if request.is_json:
            text = request.json.get("text")
            summary_content = summarizer(str(text), min_length=5, max_length=10)
            summary = str(summary_content)

    return summary