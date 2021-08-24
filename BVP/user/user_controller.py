import simplejson
from flask import request, Blueprint
from user.user_api import user_info, register_user, get_all_users, get_all_years

user_api = Blueprint('user_api', __name__)


"""API call to check valid user"""


@user_api.route('/bvp/login', methods=['POST'])
def user_login():
    email_id = request.get_json()["email_id"]
    password = request.get_json()["password"]
    timestamp = request.headers.get("Time-Stamp")
    response = user_info(email_id, password, timestamp)
    return response


@user_api.route('/bvp/user/register', methods=['POST'])
def registration():
    user_details = request.get_json()
    timestamp = request.headers.get("Time-Stamp")
    response = register_user(user_details, timestamp)
    return response


@user_api.route('/bvp/all_users', methods=['GET'])
def all_users():
    timestamp = request.headers.get("Time-Stamp")
    response = get_all_users(timestamp)
    response = simplejson.dumps(response)
    return response


@user_api.route('/bvp/user/year', methods=['GET'])
def all_years():
    timestamp = request.headers.get("Time-Stamp")
    user_id = request.headers.get("user_id")
    response = get_all_years(user_id, timestamp)
    response = simplejson.dumps(response)
    return response
