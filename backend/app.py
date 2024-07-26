import json
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token

from apis import register_blueprints, initialize_db

load_dotenv()
app = Flask(__name__)
app.config.from_pyfile('config.py')

jwt = JWTManager(app)

CORS(app)

register_blueprints(app)
initialize_db()


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response


if __name__ == '__main__':
    app.run(port=8080)
