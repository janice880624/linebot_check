from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import sys
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('5BsFIT9edUdjd+Ngk8Vm/cCankfVqTno5uQqldDc5yAxxnk3iLTsB99M4MTfIzvTpvUnOAFh5fubtt987BeCslsHpuUxsQho85MZOTc1yn3kWc2C1taEkXCGWdaKN3NxC6SxyQCP+X1mIb/1iBNFGAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f9ff6544b64a66cb362260a12dbc9529')

peos = []

class people:
    def __init__(self, thing, name, isok='!ok'):
        self.thing = thing
        self.name = name
        self.status = isok

    def getName(self):
        if self.status != 'ok':
            return self.name
        else:
            return self.name + ' V'

    def getThing(self):
        return self.thing

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        groupID = event.source.group_id
    except:
        message = TextSendMessage(text='我只接收群組內訊息，請先把我邀請到群組!')
        # line_bot_api.reply_message(event.reply_token, message)
    else:
        if not reportData.get(groupID):
            reportData[groupID]={}
        LineMessage = ''
        receivedmsg = event.message.text
        update_list = []
        final_data = []

        if '使用說明' in receivedmsg and len(receivedmsg)==4:
            LineMessage = (
                '收到以下正確格式\n'
                '才會正確記錄回報。\n'
                '----------\n'
            )

        # 測試資料 輸入資訊 媒體：烏鴉 資訊：烏鴉 敬拜團：烏鴉 其他：烏鴉
        elif '輸入資訊' in receivedmsg:
            text = receivedmsg.replace('\n', ' ').replace('\r', ' ')
            data_list = text.split(' ')
            del data_list[0]
            # data_list = ['媒體：烏鴉', '資訊：烏鴉', '敬拜團：烏鴉', '其他：烏鴉']

            LineMessage = '輸入內容如下：\n'

            for i in data_list:
                peo_f = i.split('：')
                peo = people(peo_f[0],peo_f[1],'!ok')
                peos.append(peo)

            for p in peos:
                LineMessage = LineMessage + str(p.getThing()) + ':' + str(p.getName()) +'\n'


        # 測試資料 更新 烏鴉 ok
        elif '更新' in receivedmsg:
            text2 = receivedmsg.replace('\n', ' ').replace('\r', ' ')
            update_list = text2.split(' ')
            del update_list[0]
            # update_list = ['烏鴉', 'ok']
            # new_list = [ word if i == update_list[0] else i for i in data_list]

            LineMessage = '更新內容如下：\n'

            for p in peos:
                if (p.getName() == update_list[0]):
                    p.status = 'ok'
                    # print('y')
                    # print(p.getThing(), p.getName())
                    LineMessage = LineMessage + str(p.getThing()) + ':' + str(p.getName()) +'\n'
                else:
                    # print('n')
                    # print(p.getThing(), p.getName())
                    LineMessage = LineMessage + str(p.getThing()) + ':' + str(p.getName()) +'\n'
                # LineMessage = LineMessage + str(p.getName()) + ':' + str(p.getThing()) +'\n'

        elif '清空' in receivedmsg and len(receivedmsg)==2:
            reportData[groupID].clear()
            LineMessage = '資料已重置!'
            peos.clear()

        elif '機器人掰掰' in receivedmsg and len(receivedmsg)==5:
            try:
                line_bot_api.leave_group(groupID)
                LineMessage = '掰掰!'
            except LineBotApiError as e:
                LineMessage = '嘿嘿，我還沒退出喔！'

        if LineMessage :
            message = TextSendMessage(text=LineMessage)
            line_bot_api.reply_message(event.reply_token, message)

def final(keyword, all_data):
    if keyword == 'no':
        final_data = all_data
    else:
        final_data = [ keyword if i == update_list[0] else i for i in final_data]
    return final_data

if __name__ == "__main__":
    global reportData
    reportData = {}
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
