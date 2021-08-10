from flask import request, Blueprint
from questions.questions_api import question_details, get_questions_details, upload_files_to_server
import simplejson

question_api = Blueprint('question_api', __name__)

"""API call to check valid user"""


@question_api.route('/bvp/question', methods=['POST'])
def questions():
    request_body = request.get_json()
    timestamp = request.headers.get("Time-Stamp")
    response = question_details(request_body, timestamp)
    return response


@question_api.route('/bvp/question', methods=['GET'])
def fetch_questions():
    timestamp = request.headers.get("Time-Stamp")
    user_id = request.headers.get("user_id")
    question_no = request.args['q_no']
    questions_data = get_questions_details(user_id, question_no, timestamp)
    response = simplejson.dumps(questions_data)
    return response


@question_api.route('/bvp/question/files_upload', methods=['post'])
def upload_files():
    questions_data = upload_files_to_server(request)
    response = simplejson.dumps(questions_data)
    return response
