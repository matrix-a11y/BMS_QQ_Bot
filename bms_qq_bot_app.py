import datetime
import os
import random

import pymysql
import requests
from flask import Flask, request

import getvideo

app = Flask(__name__)
database_enable = "false"

# 测试
# 还是实时同步的
# 核武器函数
# noinspection SqlResolve
# 由于tx最近严厉打击协议包
# TODO:接下来可能会进行重构
# 敬请期待

@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息状态码
        # 获取需要的消息
        Qun_id = request.get_json().get('group_id')  # 那个群发的
        QQ_name = request.get_json().get('sender').get('nickname')  # 发送者人的昵称叫啥
        QQ_id = request.get_json().get('sender').get('user_id')  # 发送者的QQ号
        Xingxi_text = request.get_json().get('raw_message')  # 发的什么东西
        xingxi_id = request.get_json().get('message_id')

        print(Qun_id)
        print(QQ_name)
        print(QQ_id)
        print(Xingxi_text)

        # 给go-cqhttp的5700端口提交数据,类似于浏览器访问的形式

        #        text = Xingxi_text  # 获取你要说的话
        #        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % text  # 这是自动聊天机器人的api接口的网址，然后把最后的参数改为获取到的你说的话
        #       response = requests.get(url)  # 使用get请求获取响应
        #        response.encoding = 'utf-8'  # 手动指定字符编码为utf-8
        #        content = "%s" % Text_Json['content']  # 获取字典content键所指的值
        #        Text_Json = json.loads(response.text)  # json.loads()是用来读取字符串的
        # Set the API key for the openai module
        # openai.api_key = "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"  # 这里放入你的key，我这里隐藏了

        # Use the GPT-3 model to generate text
        # ChatInput = Xingxi_text
        # response = openai.Completion.create(
        #    engine="text-davinci-002",
        #    prompt=ChatInput,
        #    max_tokens=1024,
        #    n=1,
        #    temperature=0.5,
        # )

        # requests.get("http://127.0.0.1:5702/send_group_msg?group_id={0}&message={1}".format(Qun_id,
        #                                                                                   response["choices"][0][
        #                                                                                       "text"]))

        if Xingxi_text == "当前时间":  # 获取时间
            time = datetime.datetime.now()
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, time))
        if Xingxi_text == "打卡":  # 打卡
            requests.get("http://127.0.0.1:5700/send_group_sign?group_id={0}".format(Qun_id))
            Success_out = "Success"
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, Success_out))
            print("打卡请求：200", Success_out)
        if Xingxi_text[0:3] == "说句话":
            tts = Xingxi_text[4:]
            msg = '[CQ:tts,text=' + tts[:220] + ']'
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, msg))
        if Xingxi_text[0:24] == "https://www.bilibili.com":
            path = 'Cachedclips'
            rcs = "已下载"
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, rcs))
            file_path = getvideo.download(Xingxi_text, path)
            file_path = "/".join(os.getcwd().split('\\')) + "/" + file_path
            name = random.randint(0, 82933902913)
            name = str(name)
            requests.get('http://127.0.0.1:5700/upload_group_file?group_id=%s&file=%s&name=%s' % (
                Qun_id, file_path, name + '.mp4'))
            getvideo.ok(path)
        if Xingxi_text[0:22] == "https://music.163.com":
            path = 'Cachedclips'
            music_path = getvideo.download(Xingxi_text, path)
            music_path = "/".join(os.getcwd().split('\\')) + "/" + music_path
            name = random.randint(1024, 27392837902)
            name = str(name)
            requests.get('http://127.0.0.1:5700/upload_group_file?group_id=%s&file=%s&name=%s' % (
                Qun_id, music_path, name + '.mp4'))
            getvideo.ok(path)
        if Xingxi_text == "文件统计":
            requests.get('http://127.0.0.1:5700/get_group_file_system_info?group_id=%s' % (Qun_id))
            file_count = request.get_json().get('file_count')  # 群里有多少文件
            limit_count = request.get_json().get('limit_count')  # 能传多少
            used_space = request.get_json().get('used_space')  # 用了多少空间
            total_space = request.get_json().get('total_space')  # 总共多少空间
            file_count = str(file_count)
            limit_count = str(limit_count)
            used_space = str(used_space)
            total_space = str(total_space)
            send_ap = "文件数量：" + file_count + "\n" + "数量上线：" + limit_count + "\n" + "已用空间：" + used_space + "\n" + "总空间：" + total_space
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, send_ap))
        # 检索敏感词并描红输出
        # 输入
        word = Xingxi_text
        # 敏感词库，自己添加词库
        sensitive = ['QQ', '加群', '你妈',
                     '你爸', '你爷', '傻逼', '人工智障', '射射',
                     '比特币', '要的联系', ]
        # 在输入语句中发现的敏感词，放在列表中
        sensitive_find = []
        # newword用于标红敏感词，word用于循环
        newword = word
        # 遍历敏感词库
        for item in sensitive:
            # 将至少出现一次的敏感词放到sensitive_find中，然后标红
            if word.count(item) > 0:
                sensitive_find.append(item + ':' + str(word.count(item)) + '次')

                # newword存放标红后的整段话，word则不变
                newword = newword.replace(item, ' \033[1;31m' + item + '\033[0m')
                # 撤回含有敏感词的消息
                requests.get("http://127.0.0.1:5700/delete_msg?message_id={0}".format(xingxi_id))
        # print('发现敏感词如下：')

        if Xingxi_text[0:6] == "添加违禁词":
            sensitive.append(Xingxi_text[7:20])
            sus_out = "添加成功"
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, sus_out))
        if Xingxi_text == "启用数据库":
            try:
                db = pymysql.connect(host="gz-cynosdbmysql-grp-qwk6hpsv.sql.tencentcdb.com",
                                     user='root',
                                     password="",
                                     database='QQ_Bot',
                                     charset='utf8',
                                     port=20795)
                requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, "已启用"))
                database_enable = "true"
            except:
                requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, "失败"))
        if Xingxi_text == "签到":
            try:
                MF = random.randint(0, 114514)
                output_text = "签到成功，获得了" + str(MF) + "积分"
                requests.get(
                    "http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, output_text))
            except:
                requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id,
                                                                                                    "系统错误，请稍后再试"))
        if Xingxi_text == "注册":
            try:
                cur = db.cursor()
                sql = """INSERT INTO Group_Member_List(Group_ID, Nickname, QQ_ID) VALUES(Qun_id,QQ_Name,QQ_id)"""
                cur.execute(sql)
                db.commit()
                requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, "成功"))
            except:
                requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, "失败"))
        if Xingxi_text == "6":
            requests.get("http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}".format(Qun_id, "9"))






    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        QQ_name_private = request.get_json().get('sender').get('nickname')  # 发送者昵称
        QQ_id_private = request.get_json().get('sender').get('user_id')  # 发送者账号
        Xingxi_text_private = request.get_json().get('raw_message')  # 信息内容
        Xingxi_id_private = request.get_json().get('message_id')

    return 'OK'  # 对go-cqhttp进行相应，不然会出现三次重试


app.run(debug=True, host='127.0.0.1', port=5701)  # 监听本机的5703端口（数据来源于go-cqhttp推送到5701端口的数据）
