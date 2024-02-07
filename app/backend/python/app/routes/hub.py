from flask import request, jsonify, make_response, Blueprint, current_app
from datetime import datetime, timedelta

hub = Blueprint('hub', __name__)


@hub.route("/hub" , methods=['POST', 'PATCH', 'DELETE', 'GET'])
def hubResonse():
  print ('hello')