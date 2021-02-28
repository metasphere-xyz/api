# interface settings

hostname = "0.0.0.0"
port = 2342

# standard routes

from flask import *
from endpoints.text.routes import text

def create_api():
    api = Flask(__name__)
    api.register_blueprint(text, url_prefix='/text')
    return api

# main route
@api.route('/', methods=['GET', 'POST'])
def welcome():
    try:
        return {
            'status': 'successful',
            'message': 'Welcome to the metasphere api.',
            'supported_endpoints': ['%s' % rule for rule in app.url_map.iter_rules()]
        }
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}

if __name__ == '__main__':
    api = create_api()
    api.run(host=hostname, port=port, debug=True)