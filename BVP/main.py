from user.user_controller import user_api
from questions.question_controller import question_api
from reports.report_controller import report_api
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.register_blueprint(user_api)
app.register_blueprint(question_api)
app.register_blueprint(report_api)


if __name__ == "__main__":
    print(app.url_map)
    from os import environ
    app.run(threaded=True, debug=False, port=environ.get("PORT", 5000))
