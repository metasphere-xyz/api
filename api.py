from endpoints.graph.routes import graph_routes
from endpoints.text.routes import text_routes
from config import *

# Configuration
api = Flask(__name__)
api.config["DEBUG"] = True
api.config["SERVER_NAME"] = 'ecchr.metasphere.xyz:2342'

# Standard routes
# CORS(api, resources=r'/text/*')


@api.route('/', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
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
api.register_blueprint(text_routes, url_prefix='/text')

# /graph
api.register_blueprint(graph_routes, url_prefix='/graph')

# TODO: add other endpoints

# Run API
if __name__ == '__main__':
    api.run(use_reloader=False)
