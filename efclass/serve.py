from flask import Flask, request, Response, json
from pymongo import MongoClient

client = MongoClient()
db = client['data-stream']

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    result = db.webpages.insert({
        'collected': dict(request.form.items())
    })
    response = Response(json.dumps({'ok': True}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Max-Age', '1000')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8716, debug=True)
