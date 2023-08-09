import requests
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
ca = certifi.where()

TTBkey: "ttbpalsied1142001"
client = MongoClient('mongodb+srv://jinhey:dbtester@cluster0.r3i3cqv.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/book", methods=["POST"])
def book_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': ogtitle,
        'desc': ogdesc,
        'image': ogimage,
        'comment': comment_receive,
        'star': star_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg': '저장완료!'})


@app.route("/book", methods=["GET"])
def book_get():
    TTBkey = "ttbpalsied1142001"
    url = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={TTBkey}&" \
          f"QueryType=ItemNewAll&MaxResults=10&start=1&SearchTarget=Book&output=js&Version=20131101"
    res = requests.get(url)
    r = res.json()['item']
    return jsonify({'result': r})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)