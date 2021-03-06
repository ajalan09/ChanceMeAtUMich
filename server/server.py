from flask import Flask , jsonify, request , render_template
from flask import Response
from urllib.parse import unquote
import requests
from flask import request
import sys
from flask_caching import Cache
import math
from model import *

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple',"CACHE_DEFAULT_TIMEOUT": 86400,'CACHE_THRESHOLD':math.inf})

f = open("model.pkl",'rb')
model = pickle.load(f)
        
@app.route("/",methods=["GET","POST"])
@cache.cached(timeout=86400, query_string=True)
def home():
    if request.method == "GET":
        return render_template('index.html')
    else:
        #convert json to data list and pass into
        content = request.form.to_dict()         
        data = [[element for key,element in content.items()]]

        for index in range(0,len(data[0])):
            if data[0][index].isnumeric():
                data[0][index]=int(data[0][index])

        data[0].append("")
        head = cleaning(data)
        result = model.predict(head)
        return jsonify({"result":int(result[0])})

#@app.errorhandler(Exception)
#def handle_exception(e):
#    """Return JSON instead of HTML for HTTP errors."""
#    # start with the correct headers and status code from the error
#    response = e.get_response()
#    # replace the body with JSON
#    response.data = json.dumps({
#        "code": e.code,
#        "name": e.name,
#        "description": e.description,
#    })
#    response.content_type = "application/json"
#    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
