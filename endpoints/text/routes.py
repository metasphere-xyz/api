from flask import *
from flask import Blueprint
from endpoints.text.functions import *
# from transformers import pipeline
# summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")
# import json

text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    json = 'application/json'
    text = 'text/plain'
    html = 'text/html'
    accept_json = request.accept_mimetypes['application/json']
    accept_text = request.accept_mimetypes['text/plain']
    accept_html = request.accept_mimetypes['text/html']

    # # HTML -> MTML
    # if request.content_type == html and accept_html==1:
        
    #     response = Response(summary, mimetype=html)

    # # TEXT/PLAIN -> TEXT/PLAIN
    # if request.content_type == text and accept_text==1:
        
    #     response = Response(summary, mimetype=text)
    
    # # TEXT/PLAIN -> APPLICATION/JSON
    # if request.content_type == text and accept_text==1:
        
    #     response = Response(summary, mimetype=json) 
    
    # # JSON -> TEXT/PLAIN
    # if request.content_type == text and accept_text==1:
        
    #     response = Response(summary, mimetype=text) 

    # JSON -> JSON
    if request.content_type == json and accept_json==1:
        if request.is_json:
            # text = request.json.get("text")
            req_json = request.get_json()
            chunk_number = len(req_json['chunk_sequence'])
            print(chunk_number)

            text_chunk = [""] * chunk_number
            compression = [0] * chunk_number
            aim_rel = [0] * chunk_number
            deviation_output = [0] * chunk_number

            for i in range(chunk_number):
                text = req_json['chunk_sequence'][i]['text']
                text_chunk[i], compression[i], aim_rel[i], deviation_output[i] = summary(text, aim=20, num_summaries=2)

            # text, compression, aim_rel, deviation_output = summary(text, aim=20, num_summaries=2)

            data = {
                "text": text_chunk,
                "compression": compression,
                "aim_rel": aim_rel,
                "deviation_output": deviation_output
                }
            response = make_response(data)
            response.mimetype=json

            return response
    
    

    return "test"
