from flask import Flask, request, Response, json
from pymongo import MongoClient

client = MongoClient('192.168.1.202')
db = client['weibo-search']

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    result = db.webpages.insert({
        'collected': dict(request.form.items()),
    })
    print(result)
    response = Response(json.dumps({'ok': True}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Max-Age', '1000')
    return response


@app.route("/seed", methods=["GET"])
def get_seed():
    doc = db.seeds.find_one({'status': 'enqueue'})
    if doc:
        seed = {'url': doc['url']}
    else:
        seed = None
    response = Response(json.dumps({'seed': seed}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Max-Age', '1000')
    if seed:
        db.seeds.update({
            '_id': doc['_id'],
        }, {
            '$set': {'status': 'pending'},
        })
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8716, debug=True)
