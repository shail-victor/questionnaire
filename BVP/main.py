from user.user_controller import user_api

from flask import Flask
from framework.get_properties import read_properties_file

app = Flask(__name__)


if __name__ == "__main__":

    app.register_blueprint(user_api)
    propList = read_properties_file('bvp_config.properties')
    if len(propList['host']) > 0:
        if len(propList['port']) > 0:
            print("Running app with both host and port")
            app.run(host=propList['host'], port=int(propList['port']), threaded=True)
        else:
            print("Running app with host")
            app.run(host=propList['host'], threaded=True)
    elif len(propList['port']) > 0:
        print("Running app with port")
        app.run(port=int(propList['port']), threaded=True)
    else:
        print("Running app with default settings")
        app.run(threaded=True)
