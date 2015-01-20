from flask import Flask, request, Response, json
from pymongo import MongoClient

client = MongoClient()
db = client['weibo-search']

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    route = request.form.get('route')
    body = request.form.get('body')
    url = request.form.get('url')
    result = db.webpages.insert({
        'route': route,
        'body': body,
        'url': url,
    })
    print(result, url)
    response = Response(json.dumps({'ok': True}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Max-Age', '1000')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8716, debug=True)
