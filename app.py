from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('', 27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/read', methods=['GET'])
def read_articles():

    result = list(db.memo.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'articles': result})

@app.route('/api/post', methods=['POST'])
def post_article():
    memo_num = db.memo.count()
    memo_num += 1
    memo_title_receive = request.form['memo_title_give']
    memo_content_receive = request.form['memo_content_give']
    memo = {'title': memo_title_receive, 'content': memo_content_receive, 'num': memo_num}

    db.memo.insert_one(memo)

    return jsonify({'result': 'success', 'msg': 'post 성공!'})

@app.route('/api/update', methods=['POST'])
def update_article():
    memo_num_receive = int(request.form['memo_num_give'])
    title_receive = request.form['memo_title_give']
    content_receive = request.form['memo_content_give']

    db.memo.update_one({'num': memo_num_receive}, {'$set': {'title': title_receive}})
    db.memo.update_one({'num': memo_num_receive}, {'$set': {'content': content_receive}})
    return jsonify({'result': 'success', 'msg': 'update 성공!'})

@app.route('/api/delete', methods=['POST'])
def delete_article():
    memo_num_receive = int(request.form['num_give'])
    db.memo.delete_one({'num': memo_num_receive})

    return jsonify({'result': 'success', 'msg': 'delete 성공!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
