import random
from flask import Flask, request, abort
from decouple import config
from pymongo import MongoClient
import json
from bson import json_util

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from util import *


MONGO_URL=config('MONGO_URL')
IMAGE_PATH=config('IMAGE_PATH')
PORT=config('PORT')

cluster=MongoClient(MONGO_URL)
db=cluster['mahjong']
db_people=db['people']
app=Flask(__name__)
line_bot_api = LineBotApi('O91dI/Dha57YpV+HsZkquETJFrEsHpZZ2kmyTOMeRGojBSgTVbMyPijyXN8J9Gn351eejlUOU/93Ol/mgIKZYas9kVAW+YDKB/PpYxRgiZw1UsnZewK0ylKGctzG9pZDxbtUWdjkaSXkrm8/uZIyYAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('13e4f47b2ab2b7453bd86a827d09bae1')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

@app.route('/list-all',methods=['GET'])
def list_people():
    all_people=list(db_people.find({}))
    return json.dumps(all_people,default=json_util.default)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    
    with open(IMAGE_PATH, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    try:
        info=get_info(IMAGE_PATH)
        points=get_point(info)
        for p in points:
            exist_person=db_people.find_one({"name":p['name']})   
            new_score=p["score"]
            if exist_person:
                new_score+=exist_person["score"]
                db_people.find_one_and_update({"name":p['name']},{"$set":{"score":new_score}},upsert=True)
                TextSendMessage(text='update person to:'+str({"name":p['name'],"score":new_score}))
                print('update person to:'+str({"name":p['name'],"score":new_score}))
            else:
                db_people.insert_one({"name":p["name"],"score":new_score})
                TextSendMessage(text='add a new person:'+str(p))
                print('add a new person:'+str(p))
    except:
        print('error')
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="圖片解析錯誤，請重新上傳"))
        
if __name__=='__main__':
    app.run(debug=True,port=PORT)
    