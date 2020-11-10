from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle
# db.memo.insert_one({'num': 0, 'title': 'example', 'content': 'content_example'})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/read', methods=['GET'])
def read_articles():

    result = list(db.memo.find({}, {'_id': 0})) #id도 받아온다!

    return jsonify({'result': 'success', 'articles': result})

@app.route('/api/post', methods=['POST'])
def post_article():
    memo_title_receive = request.form['memo_title_give']
    memo_content_receive = request.form['memo_content_give']
    memo = {'title': memo_title_receive, 'content': memo_content_receive}

    db.memo.insert_one(memo)

    return jsonify({'result': 'success', 'msg': 'post 성공!'})

@app.route('/api/update', methods=['POST'])
def update_article():
    title_original = request.form['title_original_give']
    title_receive = request.form['memo_title_give']
    content_receive = request.form['memo_content_give']

    #각각의 메모가 타이틀이 달라야 올바른 검색이 가능하다는 것은 조금 아쉽다. db의 id로 연결해야 하는 것이 맞는 것 같은데...
    db.memo.update_one({'title': title_original}, {'$set': {'title': title_receive}})
    db.memo.update_one({'title': title_original}, {'$set': {'content': content_receive}})
    return jsonify({'result': 'success', 'msg': 'update 성공!'})

@app.route('/api/delete', methods=['POST'])
def delete_article():
    memo_title_receive = request.form['memo_title']
    db.memo.delete_one({'title': memo_title_receive})

    return jsonify({'result': 'success', 'msg': 'delete 성공!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
