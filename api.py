from flask import *
import traceback
from functions import *

# Configuration
api = Flask(__name__)
api.config["DEBUG"] = True
# api.config["SERVER_NAME"] = 'ecchr.metasphere.xyz:2342'

# Standard routes
@api.route('/', methods=['GET', 'POST'])
def welcome():
    try:
        return {
            'status': 'success',
            'message': 'Welcome to the metasphere api!',
            'request type': request_type(request),
            'response type': response_type(request),
            'supported_endpoints': ['%s' % rule for rule in api.url_map.iter_rules()]
        }
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}

# Endpoints
# /text/
from endpoints.text.routes import text
api.register_blueprint(text, url_prefix='/text')

# /graph
from endpoints.graph.routes import graph
api.register_blueprint(graph, url_prefix='/graph')

# TODO: add other endpoints

# Run API
if __name__ == '__main__':
    api.run()