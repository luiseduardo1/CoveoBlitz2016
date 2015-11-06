#!../bin/env python

import json
import Team
from flask import Flask, request,Response, abort

app = Flask(__name__)
responseWriter = Team.createResponseWriter()


class NonASCIIJSONEncoder(json.JSONEncoder):
    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(NonASCIIJSONEncoder, self).__init__(**kwargs)

@app.route('/CoveoBlitz', methods=['POST'])
def createAnswer():
    if not request.get_json() or not 'q' in request.get_json():
        abort(400)
    
    content = request.get_json()
    responseWriter.parseRequest(content)
    answerJSON = json.dumps(responseWriter.serializeJSON(), cls=NonASCIIJSONEncoder)
    response = Response(response=answerJSON,
               status=200,
               mimetype="application/json")
    
    responseWriter.matchedParagraphs.clear()
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
