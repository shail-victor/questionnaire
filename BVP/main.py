from user.user_controller import user_api
from questions.question_controller import question_api
from reports.report_controller import report_api
from flask import Flask
from framework.get_properties import read_properties_file
from flask_cors import CORS
import os

app = Flask(__name__)
#CORS(app)


app.register_blueprint(user_api)


if __name__ == "__main__":
    # registering user API's
    # Registering questions API's
    app.register_blueprint(question_api)
    app.register_blueprint(report_api)
    print("searching for URL")
    app.run(threaded=True, port=5000)
