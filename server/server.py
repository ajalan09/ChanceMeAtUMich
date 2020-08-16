from flask import Flask , jsonify, request
from flask import Response
from urllib.parse import unquote
import requests
from flask import request
import sys
from flask_caching import Cache
import math

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple',"CACHE_DEFAULT_TIMEOUT": 86400,'CACHE_THRESHOLD':math.inf})
        
@app.route("/",methods=["GET","POST"])
@cache.cached(timeout=86400, query_string=True)
def home():
    if request.method == "GET":
        content = request.json
        return jsonify({"success":200})

@app.route('/list',methods=['GET'])
@cache.cached(timeout=86400, query_string=True)
def list():
    pass

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)