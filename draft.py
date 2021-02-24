from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
# @accept('plain/text')
def accept_json():
    if request.is_json: 
        return (request.data,"valid json")
    else:
        return "bad"
    

@app.route('/valid_content', methods=['GET', 'POST'])
def valid_content():
    if request.content_type == 'text/plain':

        return Response("valid text", mimetype='application/json')
    elif request.accept_mimetypes["plain/text"]:
        return "text"
    elif request.content_type == 'application/json':
        if request.is_json: 
        return (request.data,"valid json")

        return Response(request.data, mimetype='application/json')
    else:
        return Response("no text/ no json", mimetype='text/plain')

def return_accepted_requests(response):
    if request.accept_mimetypes["plain/text"]:
        return Response(response, mimetype='text/plain')
    if request.accept_mimetypes["application/json"]:
        if not response.is_json:
            response = jsonify(response)
        return Response(response, mimetype='application/json')

@app.route('summarize')
def summarize():
    if request.content_type == 'text/plain':
        text = request
    if request.content_type == 'application/json':
        if request.is_json:
            text = jsonObject['text']
            aim = jsonObject['aim']
            # fortführen
    [result, deviation, compression] = summarize(text, aim)
    
    # Response Object richtig codieren
    if request.accept_mimetypes["application/json"]:
        # Json object konstruieren -> response (prüfen ob json)
        response = jsonify(response)
    elif request.accept_mimetypes["text/plain"]:
        response = result
    return return_accepted_requests(response)

    
    
if __name__ == '__main__':
    app.run(debug=True)