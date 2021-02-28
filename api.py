from flask import *
from endpoints.text.routes import text

def create_api():
    api = Flask(__name__)

    @api.route('/', methods=['GET', 'POST'])
    def home():
        return "Welcome Home!"

    api.register_blueprint(text, url_prefix='/text')

    return api
    
if __name__ == '__main__':
    api = create_api()
    api.run(host='0.0.0.0', port=2342, debug=True)
