from user.user_controller import user_api
from questions.question_controller import question_api
from reports.report_controller import report_api
from flask import Flask
from framework.get_properties import read_properties_file
from flask_cors import CORS
import os

app = Flask(__name__)
#CORS(app)


if __name__ == "__main__":
    # registering user API's
    app.register_blueprint(user_api)
    # Registering questions API's
    app.register_blueprint(question_api)
    app.register_blueprint(report_api)
    #propList = read_properties_file('bvp_config.properties')
    # if len(propList['host']) > 0:
    #     if len(os.environ.get("PORT", propList['port'])) > 0:
    #         print("Running app with both host and port")
    #         app.run(host=propList['host'], port=int(os.environ.get("PORT", propList['port'])), threaded=True)
    #     else:
    #         print("Running app with host")
    #         app.run(host=propList['host'], threaded=True)
    # elif len(os.environ.get("PORT", propList['port'])) > 0:
    #     print("Running app with port")
    #     app.run(port=int(os.environ.get("PORT", propList['port'])), threaded=True)
    # else:
    #     print("Running app with default settings")
    #     app.run(threaded=True)

    #port = int(os.environ.get("PORT", 5000))
    print("searching for URL")
    app.run()
