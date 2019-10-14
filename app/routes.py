import logging

import flask
from flask import Response, request
from fetch_api import MergedApi
import json
app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)

api = MergedApi()
@app.route('/team', methods=["GET"])
def team_info():
    api.team_name = request.args.get('name')
    merged_team_info = api.getMergedTeam()
    json_merged_team_info = json.dumps(merged_team_info)
    json_response = app.response_class(
        response=json_merged_team_info,
        mimetype='application/json'
    )
    return json_response
