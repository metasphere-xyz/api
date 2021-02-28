from flask import *
import traceback
from functions import *

# Configuration
api = Flask(__name__)
api.config["DEBUG"] = True
api.config["SERVER_NAME"] = 'ecchr.metasphere.xyz:2342'

# Standard routes
@api.route('/', methods=['GET', 'POST'])
def welcome():
    try:
        return {
            'status': 'success',
            'request type': request_type(request),
            'response type': response_type(request),
            'message': 'Welcome to the metasphere api!',
            'supported_endpoints': ['%s' % rule for rule in api.url_map.iter_rules()]
        }
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}

# Endpoints
from endpoints.text.routes import text
api.register_blueprint(text, url_prefix='/text')

# Run API
if __name__ == '__main__':
    api.run()