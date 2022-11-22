import datetime
import json
import os
import random

import requests
from flask import Flask, request

import getvideo

app = Flask(__name__)


# 核武器函数
@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息状态码
        # 获取需要的消息
        Qun_id = request.get_json().get('group_id')  # 那个群发的
        QQ_name = request.get_json().get('sender').get('nickname')  # 发送者人的昵称叫啥
        QQ_id = request.get_json().get('sender').get('user_id')  # 发送者的QQ号
        Xingxi_text = request.get_json().get('raw_message')  # 发的什么东西
        print(Qun_id)
        print(QQ_name)
        print(QQ_id)
        print(Xingxi_text)

        # 给go-cqhttp的5700端口提交数据,类似于浏览器访问的形式

        text = Xingxi_text  # 获取你要说的话
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % text  # 这是自动聊天机器人的api接口的网址，然后把最后的参数改为获取到的你说的话
        response = requests.get(url)  # 使用get请求获取响应
        response.encoding = 'utf-8'  # 手动指定字符编码为utf-8
        Text_Json = json.loads(response.text)  # json.loads()是用来读取字符串的
        content = "%s" % Text_Json['content']  # 获取字典content键所指的值

        requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, content))
        if Xingxi_text == "菜单":  # 菜单
            ap = (
                "～～【群管系统】～～入群审核      入群欢迎入群改名      自主通知链接检测      名片锁定定时任务      入群验证广告词检测   敏感词检测白名单设置   黑名单设置关键词回复   撤回系统")
            requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, ap))
        if Xingxi_text == "当前时间":  # 获取时间
            time = datetime.datetime.now()
            requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, time))
        if Xingxi_text == "打卡":  # 打卡
            requests.get("http://127.0.0.1:5702/send_group_sign?group_id={0}".format(Qun_id))
            Success_out = "Success"
            requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, Success_out))
            print("打卡请求：200", Success_out)
        if Xingxi_text[0:3] == "说句话":
            tts = Xingxi_text[4:]
            msg = '[CQ:tts,text=' + tts[:220] + ']'
            requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, msg))
        if Xingxi_text[0:23] == "https://www.bilibili.com":
            path = 'Cachedclips'
            rcs = "已下载"
            requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id, rcs))
            file_path = getvideo.download(Xingxi_text, path)
            file_path = "/".join(os.getcwd().split('\\')) + "/" + file_path
            name = random.randint(0, 82933902913)
            name = str(name)
            requests.get('http://127.0.0.1:5702/upload_group_file?group_id=%s&file=%s&name=%s' % (
            Qun_id, file_path, name + '.mp4'))
            getvideo.ok(path)
        if Xingxi_text[0:16] == "https://music.163.com":
            path = 'Cachedclips'
            music_path = getvideo.download(Xingxi_text, path)
            music_path = "/".join(os.getcwd().split('\\')) + "/" + music_path
            name = random.randint(1024, 27392837902)
            name = str(name)
            requests.get('http://127.0.0.1:5702/upload_group_file?group_id=%s&file=%s&name=%s' % (
            Qun_id, music_path, name + '.mp3'))



    return 'OK'  # 对go-cqhttp进行相应，不然会出现三次重试


app.run(debug=True, host='127.0.0.1', port=5703)  # 监听本机的5703端口（数据来源于go-cqhttp推送到5701端口的数据）
