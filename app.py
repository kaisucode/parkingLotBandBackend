from flask import Flask, request, jsonify, redirect, session, url_for, send_file
from flask_cors import CORS, cross_origin
import json
import uuid
import os
import time
from datetime import datetime

PORT = "5000"
app = Flask(__name__)

# CORS
#  origin = "http://localhost:3000"
origin = "*"
CORS(app, resources={r"*": {"origins": origin, "supports_credentials": True}})

@app.route("/generateTrack/", methods=["POST"])
@cross_origin()
def generateTrack(): 

    isFile = request.json["isFile"]
    if (!isFile): 

    return_json = {"status": "success", 'music_files': aFile, "id": id}
    return json.dumps(return_json, default=str), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)

