from flask import *
from flask import Blueprint
from endpoints.text.functions import *
import json

text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    # Input Parameter: Summary
    aim = 50
    deviation = 10
    num_summaries = 1

    app_json = 'application/json'
    text = 'text/plain'
    html = 'text/html'
    accept_json = request.accept_mimetypes['application/json']
    accept_text = request.accept_mimetypes['text/plain']
    accept_html = request.accept_mimetypes['text/html']

    # JSON -> JSON
    if request.content_type == app_json and accept_json==1:

        data = {
                "chunk_sequence": [ 
                ]
            }
            
        if request.is_json:
            req_json = request.get_json()
            chunk_number = len(req_json["chunk_sequence"])

            text_chunk = [""] * chunk_number
            compression = [0] * chunk_number
            aim_rel = [0] * chunk_number
            deviation_output = [0] * chunk_number
            
            for i in range(chunk_number):

                data["chunk_sequence"].append(
                    {
                        "chunk_id": i,
                        "summary": [
                        ]
                    }
                )

                text = req_json["chunk_sequence"][i]["text"]
                text_chunk[i], compression[i], aim_rel[i], deviation_output[i] = summary(text, aim=aim, deviation_input=deviation, num_summaries=num_summaries, chunk_number=chunk_number)
                
                if num_summaries>1:
                    for j in range(num_summaries):
                        data["chunk_sequence"][i]["summary"].append(
                            {
                                "text": text_chunk[i][j],
                                "summary_id": j,
                                "compression": compression[i][j],
                                "aim": aim_rel[i][j],
                                "deviation": deviation_output[i][j]
                            },
                        )
                else:
                    data["chunk_sequence"][i]["summary"].append(
                            {
                                "text": text_chunk[i],
                                "summary_id": i,
                                "compression": compression[i],
                                "aim": aim_rel[i],
                                "deviation": deviation_output[i]
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
