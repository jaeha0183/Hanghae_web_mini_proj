import requests
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask_cors import CORS
import certifi

ca = certifi.where()
TTBkey: "ttbpalsied1142001"
client = MongoClient('mongodb+srv://jinhey:dbtester@cluster0.r3i3cqv.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)
CORS(app)


@app.route('/main')
def main():
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_get():
    id_receive = request.form['id_gives']
    pw_receive = request.form['pw_gives']
    result = db.users.find_one({'id': id_receive, 'pw': pw_receive})

    if result is not None:
        return jsonify({'result': 'success', 'msg': '로그인 성공!'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    pw_receive = request.form['pw_give']

    doc = {
    'name':name_receive,
    'id':id_receive,
    'pw':pw_receive
    }
    results = db.users.find_one({'id': id_receive},{'_id':False})

    if results is None:
        db.users.insert_one(doc)
        return jsonify({'result': 'success','msg':'회원가입 완료!'})
    else:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 ID입니다. 다른 ID를 사용하십시오.'})


@app.route('/myreport')
def myreport():
    return render_template('myreport.html')


@app.route("/book", methods=["GET"])
def book_get():
    TTBkey = "ttbpalsied1142001"
    url = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={TTBkey}&" \
          f"QueryType=Bestseller&MaxResults=32&start=1&SearchTarget=Book&output=js&Version=20131101&cover=Big"
    res = requests.get(url)
    r = res.json()['item']
    print(r[0]['isbn'])
    return jsonify({'result': r})


@app.route("/book/search", methods=["POST"])
def book_search():
    search_value = request.form['search_value']
    print(search_value)
    TTBkey = "ttbpalsied1142001"
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={TTBkey}&Query={search_value}&QueryType=Title&MaxResults=32&start=1&SearchTarget=Book&output=js&Version=20131101&cover=Big"
    res = requests.get(url)
    r = res.json()['item']
    return jsonify({'result': r})


@app.route("/book_save", methods=["POST"])
def book_save():
    userID_receive = request.form['userID_give']
    star_chan_receive = request.form['star_chan_give']
    comment_chan_receive = request.form['comment_chan_give']
    author_receive = request.form['author_give']
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    pubDate_receive = request.form['pubDate_give']
    isbn_receive = request.form['isbn_give']
    itemId_receive = request.form['itemId_give']
    descSub_receive = request.form['descSub_give']

    doc = {
        'userID' : userID_receive,
        'star': star_chan_receive,
        'comment': comment_chan_receive,
        'author': author_receive,
        'title': title_receive,
        'image': image_receive,
        'pubDate': pubDate_receive,
        'isbn': isbn_receive,
        'itemId': itemId_receive,
        'descSub': descSub_receive
    }
    db.userinfo.insert_one(doc)
    return jsonify({'msg': '저장완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)