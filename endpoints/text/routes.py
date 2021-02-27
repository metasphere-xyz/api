from flask import *
from flask import Blueprint
from endpoints.text.functions import *
import json

text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    # Input Parameter: Summary
    # aim = 20
    # deviation = 15
    # num_summaries = 1

    app_json = 'application/json'
    text = 'text/plain'
    html = 'text/html'
    accept_json = request.accept_mimetypes['application/json']
    accept_text = request.accept_mimetypes['text/plain']
    accept_html = request.accept_mimetypes['text/html']

    # JSON -> JSON
    if request.content_type == app_json and accept_json==1:

        data = {
                "chunk_id": "md5sum",
                "summary": [ 
                ]
            }
            
        if request.is_json:
            req_json = request.get_json()

            text = req_json["text"]
            aim = req_json["aim"]
            deviation = req_json["deviation"]
            num_summaries = req_json["num_summaries"]

            text_chunk = [""] * num_summaries
            compression = [0] * num_summaries
            aim_rel = [0] * num_summaries
            deviation_output = [0] * num_summaries

            # Generate n>1 summaries by multiple summary call -> no num_summaries case distinction
            text_chunk, compression, aim_rel, deviation_output = summary(text, aim=aim, deviation_input=deviation, num_summaries=num_summaries)

            if num_summaries>1:
                for i in range(num_summaries):
                    data["summary"].append(
                        {
                            "text": text_chunk[i],
                            "summary_id": i,
                            "compression": compression[i],
                            "aim": aim_rel[i],
                            "deviation": deviation_output[i]
                        },
                    )
            else: 
                data["summary"].append(
                        {
                            "text": text_chunk,
                            "summary_id": 1,
                            "compression": compression,
                            "aim": aim_rel,
                            "deviation": deviation_output
                        },
                    )

            data_json = json.dumps(data)
            response = make_response(data_json)
            response.mimetype=app_json

            return response
    
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
    
    return "endpoint: summary"
