import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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

# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image_message(event):
    