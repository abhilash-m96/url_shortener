import environs
import sys
from flask import Flask
from flask_restful import Api
from environs import Env

from resources.shorten import Shorten
from resources.url_redirector import URLRedirector

app = Flask(__name__)
api = Api(app)

# APP configs
env = Env()
env.read_env()


try:
    app.config["MONGODB_SETTINGS"] = {
        "db": env("DATABASE"),
        "host": env("MONGO_HOST"),
        "username": env("USER_NAME"),
        "password": env("PASSWORD"),
        "port": env.int("MONGO_PORT"),
    }

    app.config["DEBUG"] = env.bool("DEBUG")
    app.config["PORT"] = env.int("PORT")
except environs.EnvError as e:
    print("Configuration Issue, please check!")
    print(str(e))
    sys.exit(1)


api.add_resource(Shorten, "/shorten")
api.add_resource(URLRedirector, "/<string:shortened_id>")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=app.config["PORT"], debug=app.config["DEBUG"])
