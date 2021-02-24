from flask import *
from flask import Blueprint
from endpoints.text.functions import *

text = Blueprint('text', __name__)

@text.route('/summarize', methods=['POST', 'GET'])
def summarize():
    