import requests
import json


def ai(text):

    text = input("你说：")  # 获取你要说的话
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % text  # 这是自动聊天机器人的api接口的网址，然后把最后的参数改为获取到的你说的话
    response = requests.get(url)  # 使用get请求获取响应
    response.encoding = 'utf-8'  # 手动指定字符编码为utf-8
    Text_Json = json.loads(response.text)  # json.loads()是用来读取字符串的
    content = "机器人：%s" % Text_Json['content']  # 获取字典content键所指的值

    return content  # 打印出机器人所说的话


