from flask import Flask, request
import requests
app = Flask(__name__)

@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'private':          # 如果是私聊信息
        QQ_name = request.get_json().get('sender').get('nickname')        # 发送者昵称
        QQ_id = request.get_json().get('sender').get('user_id')           # 发送者账号
        Xingxi_text = request.get_json().get('raw_message')               # 信息内容
        Xingxi_id = request.get_json().get('message_id')                  # 信息ID
        requests.get("http://127.0.0.1:5700/send_private_msg?user_id=%s&message=%s" % (QQ_id,Xingxi_text) )

    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5701)  # 此处的 host和 port对应上面 yml文件的设置
