import datetime as dt
import os
import random as rd
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import autojoin as aj

import bili
import findbd
import pts
qxbz = {'0520':[], '0810':[], '1024':[], '1040':[], '1145':[],'1314':[], '1919':[], '2048':[], '2240':[], '2345':[]}
kwqzd = ['0520', '0810', '1024', '1040', '1145']
kwxbz = ['1314', '1919', '2048', '2240', '2345']
where = 'http://127.0.0.2:5700/'
hdrs = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
zxbz = []

def refresh(i, d):
    try:
        rsps = requests.get("https://yinchuanbus.miraheze.org/wiki/用户:" + d[i][0])
        print(d[i][0])
        rsps = BeautifulSoup(rsps.text, "html.parser")
        newedit = rsps.find("div", {"id": 'siteSub'}).string
        newedit = newedit.split('次')[0]
        newedit = int(newedit)
        d[i][1] += (newedit-d[i][2])*10
        d[i][2] = newedit
        if (newedit - d[i][2]) != 0:
            rsps = requests.get(
                "https://yinchuanbus.miraheze.org/w/index.php?title=特殊:用户贡献/%s&offset=&limit=%s" % (
                d[i][0], (newedit - d[i][2])))
            qsqs = BeautifulSoup(rsps.text, "html.parser")
            sth = [int(''.join(x.string[1:].split(','))) for x in qsqs.find_all('strong', {'class': 'mw-diff-bytes'})]
            for i in sth:
                d[i][2] += i / 50
            print('awa')
    except:
        pass
    return d


cc = 0
odid = 0
tm = 0
fs = False
is_downloading1 = False
is_downloading2 = False
event_queue1 = []
event_queue2 = []
app = Flask(__name__)
qqy_dict = {}


@app.route('/', methods=["POST"])
def post_data():
    global odid, is_downloading1, event_queue1, is_downloading2, event_queue2, qqy_dict, tm, where, kwqzd, kwxbz, cc, zxbz,qxbz
    now = dt.datetime.now()
    if(now.hour == now.minute and now.minute == 0 and now.second <= 10):
        qqy_dict = {}
        kwqzd = ['0520','0810','1024','1040','1145']
        kwxbz = ['1314','1919','2048','2240','2345']
        qxbz = {'0520':[], '0810':[], '1024':[], '1040':[], '1145':[],'1314':[], '1919':[], '2048':[], '2240':[], '2345':[]}
        zxbz = []
        requests.get(where+"set_restart?&delay=2000")
    if(len(kwqzd)):
        if(now.hour<=12 and now.hour>=int(kwqzd[0][:2]) and now.minute>=int(kwqzd[0][2:]) and now.second<=10):
            kwqzdh = int(kwqzd[0][:2])
            kwqzdm = int(kwqzd[0][2:])
            cc = kwqzd[0]
            del kwqzd[0]
            n = requests.get((where+'send_group_msg?&group_id=587827174&message=现在是北京时间%s:%s分，开往%s的轨道交通1号线即将发车，请您有序上车，漏乘请补票，发送“%s”买票上车，发送“%s往返”购买往返票上车。' % (kwqzdh, kwqzdm, "群主邸", cc, cc)))
            print(n.json())
    if(len(kwxbz)):
        if(now.hour>12 and now.hour>=int(kwxbz[0][:2]) and now.minute>=int(kwxbz[0][2:]) and now.second<=10 and len(kwxbz)):
            kwxbzh = int(kwxbz[0][:2])
            kwxbzm = int(kwxbz[0][2:])
            cc = kwxbz[0]
            del kwxbz[0]
            n = requests.get((where + 'send_group_msg?&group_id=587827174&message=现在是北京时间%s:%s分，开往%s的轨道交通1号线即将发车，请您有序上车，漏乘请补票，购买往返票的乘客请不要漏乘返回班次，发送“%s”买票上车。' % (kwxbzh, kwxbzm, "下北泽", cc)))
            print(n.json())
    from_ = request.get_json()
    pstt = from_['post_type']
    try:
        pass
    except:
        pass
    else:
        if(pstt=='meta_event'):
            tm+=1
            if(tm%12==0):
                try:
                    with open("users.json",'r', encoding='utf-8') as f:
                        dod = eval(f.read())
                    for i in dod:
                        newl = refresh(i,dod)
                        if(newl[i][1]!=dod[i][1]):
                            msg = str(newl[i][1]-dod[i][1])
                            requests.get(where+'send_group_msg?group_id=%s&message=%s' % ('587827174', '[CQ:at,qq=' + i + ']感谢你为我们的wiki添砖加瓦！恭喜你喜提明奈币：' + msg))
                        with open("users.json",'w',encoding='utf-8') as f:
                            f.write(str(newl))
                except Exception as e:
                    print(e)
        elif(pstt=='request'):
            QQ_id = from_['user_id']
            if(from_['request_type']=='group'):
                grp_id = from_['group_id']
                if(grp_id==587827174):
                    flg = from_['flag']
                    requests.get(where+'set_group_add_request?&flag=%s&sub_type=add&approve=%s'%(flg,aj.check(from_['comment'],QQ_id)))
                    if(aj.check(from_['comment'],QQ_id)):
                        with open("users.json","r+",encoding='utf-8') as f:
                            d = eval(f.read())
                            d[str(QQ_id)] = [from_['comment'],0,0]
                            f.seek(0)
                            f.write(str(d))
                    return 'ok'
            else:
                return 'ok'
        elif(pstt=='message'):
            msg_type = from_['message_type']
            Message = from_['raw_message']
            Message_id = from_['message_id']
            QQ_id = from_['user_id']
            if(odid==Message_id):
                return 'ok'
            odid = Message_id
            if(msg_type=='group'):
                grp_id = from_['group_id']
                if(os.path.exists('diy/m'+str(grp_id)+'.py')):
                    exec('import diy.m'+str(grp_id)+' as m;m.do(from_);')
                if(Message=="查询明奈币" and grp_id==587827174):
                    with open("users.json",'r',encoding='utf-8') as f:
                        d=eval(f.read())
                    d = refresh(str(QQ_id),d)
                    with open("users.json",'w',encoding='utf-8') as f:
                        f.write(str(d))
                    msg = str(d[str(QQ_id)][1])
                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                        grp_id, '[CQ:at,qq=' + str(QQ_id) + ']所拥有的明奈币为：' + msg))
                if (Message == cc and grp_id == 587827174):
                    hhh = int(cc[:2])
                    mmm = int(cc[2:])
                    if(hhh<=12):
                        if(not QQ_id in zxbz):
                            zxbz.append(QQ_id)
                        else:
                            msg = "捏已经在终点了（"
                            requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                grp_id, '[CQ:at,qq=' + str(QQ_id) + ']' + msg))
                            return 'ok'
                    else:
                        if(QQ_id in zxbz):
                            del zxbz[QQ_id]
                        else:
                            msg = "捏已经在终点了（"
                            requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                grp_id, '[CQ:at,qq=' + str(QQ_id) + ']' + msg))
                            return 'ok'
                    if(hhh==now.hour and mmm==now.minute):
                        if(QQ_id in qxbz[cc]):
                            msg = '来啦~快回吧）'
                        else:
                            with open("users.json", 'r', encoding='utf-8') as f:
                                d = eval(f.read())
                            if(rd.randint(1,100)==8):
                                msg = 'ohhhhh 恭喜你是今天的幸运儿！免票！'
                            elif(rd.randint(1,100)<=10):
                                msg = '恭喜你喜提八折票！'
                                d[str(QQ_id)][1]-=16
                            elif(rd.randint(1,100)>=70):
                                msg = '九折票诶！你今天的运气爆棚！'
                                d[str(QQ_id)][1]-=18
                            else:
                                msg = '欢迎乘坐！扣费20明奈币~'
                                d[str(QQ_id)][1]-=20
                            with open("users.json", 'w', encoding='utf-8') as f:
                                f.write(str(d))
                        requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                            grp_id, '[CQ:at,qq=' + str(QQ_id) + ']'+msg))
                    else:
                        if(QQ_id in qxbz[cc]):
                            with open("users.json", 'r', encoding='utf-8') as f:
                                d = eval(f.read())
                            d[str(QQ_id)][1]-=15
                            with open("users.json", 'w', encoding='utf-8') as f:
                                f.write(str(d))
                            requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                grp_id, '[CQ:at,qq=' + str(QQ_id) + ']您漏乘力，给我付币子，三十啊三十的一半（恼'))
                        else:
                            with open("users.json", 'r', encoding='utf-8') as f:
                                d = eval(f.read())
                            d[str(QQ_id)][1]-=30
                            with open("users.json", 'w', encoding='utf-8') as f:
                                f.write(str(d))
                            requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                grp_id, '[CQ:at,qq=' + str(QQ_id) + ']您漏乘力，给我付币子，三十啊三十（恼'))
                if (Message == str(cc)+"往返" and grp_id == 587827174 and (int(cc[:2])<12)):
                    qxbz[kwxbz[4-len(kwqzd)]].append(QQ_id)
                    hhh = int(cc[:2])
                    mmm = int(cc[2:])
                    if not QQ_id in zxbz:
                        zxbz.append(QQ_id)
                    else:
                        msg = "捏已经在终点了（"
                        requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                            grp_id, '[CQ:at,qq=' + str(QQ_id) + ']' + msg))
                        return 'ok'
                    if (hhh == now.hour and mmm == now.minute):
                        with open("users.json", 'r', encoding='utf-8') as f:
                            d = eval(f.read())
                        if (rd.randint(1, 100) == 8):
                            msg = 'ohhhhh 恭喜你是今天的幸运儿！免票！\n也请记得在%s时回来嗷~' % (kwxbz[4-len(kwqzd)][:2]+':'+kwxbz[4-len(kwqzd)][2:])
                        elif (rd.randint(1, 100) <= 10):
                            msg = '恭喜你喜提八折票！\n也请记得在%s时回来嗷~' % (kwxbz[4-len(kwqzd)][:2]+':'+kwxbz[4-len(kwqzd)][2:])
                            d[str(QQ_id)][1] -= 35*0.8
                        elif (rd.randint(1, 100) >= 70):
                            msg = '九折票诶！你今天的运气爆棚！\n也请记得在%s时回来嗷~' % (kwxbz[4-len(kwqzd)][:2]+':'+kwxbz[4-len(kwqzd)][2:])
                            d[str(QQ_id)][1] -= 35*0.9
                        else:
                            msg = '欢迎乘坐！扣费35明奈币~\n也请记得在%s时回来嗷~'% (kwxbz[4-len(kwqzd)][:2]+':'+kwxbz[4-len(kwqzd)][2:])
                            d[str(QQ_id)][1] -= 35
                        with open("users.json", 'w', encoding='utf-8') as f:
                            f.write(str(d))
                        requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                            grp_id, '[CQ:at,qq=' + str(QQ_id) + ']' + msg))
                    else:
                        with open("users.json", 'r', encoding='utf-8') as f:
                            d = eval(f.read())
                        d[str(QQ_id)][1] -= 40
                        with open("users.json", 'w', encoding='utf-8') as f:
                            f.write(str(d))
                        requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                            grp_id, '[CQ:at,qq=' + str(QQ_id) + ']先把前面的票补了再说（\n给我付币子，四十啊四十（恼\n回来是%s，憋再漏乘了嗷'% (kwxbz[4-len(kwqzd)][:2]+':'+kwxbz[4-len(kwqzd)][2:])))
                if(Message=='签到'):
                    if (str(QQ_id) in qqy_dict):
                        if (qqy_dict[str(QQ_id)] >= 2):
                            requests.get(where + 'set_group_ban?group_id=%s&user_id=%s&duration=%s' % (
                            grp_id, str(QQ_id),
                            min(29 * 86400 + 59 * 60, 60 * qqy_dict[str(QQ_id)] ** qqy_dict[str(QQ_id)])))
                        else:
                            requests.get(where+'send_group_msg?group_id=%s&message=%s' % (grp_id, '佛祖已经开始不高兴了，准备好被功德-1'))
                    else:
                        if(grp_id==587827174):
                            with open("users.json", 'r',encoding='utf-8') as f:
                                d = eval(f.read())
                            if(d[str(QQ_id)][1]<0):
                                sjs = rd.randint(1, 100)*0.8
                                requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                    grp_id,
                                    '[CQ:at,qq=' + str(QQ_id) + ']签到成功，今日的功德为：' + str(sjs)))
                                qqy_dict[str(QQ_id)] = 1
                            else:
                                sjs = rd.randint(1, 100)
                                requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                                    grp_id,
                                    '[CQ:at,qq=' + str(QQ_id) + ']签到成功，今日的功德为：' + str(
                                        sjs)))
                                qqy_dict[str(QQ_id)] = 1
                            with open("users.json",'w',encoding='utf-8') as f:
                                d[str(QQ_id)][1]+=sjs/10
                                f.write(str(d))
                        else:
                            requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (
                            grp_id, '[CQ:at,qq=' + str(QQ_id) + ']签到成功，今日的功德为：' + str(rd.randint(1, 100))))
                            qqy_dict[str(QQ_id)] = 1
                if(Message=='娶群友'):
                    if(QQ_id==3457033615):
                        return 'ok'
                    if(str(QQ_id) in qqy_dict):
                        if(qqy_dict[str(QQ_id)]>=2):
                            requests.get(where+'set_group_ban?group_id=%s&user_id=%s&duration=%s'%(grp_id,str(QQ_id),min(29*86400+59*60,60*qqy_dict[str(QQ_id)]**qqy_dict[str(QQ_id)])))
                        else:
                            requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'功德-114514'))
                        qqy_dict[str(QQ_id)]+=1
                    else:
                        if (grp_id == 587827174):
                            with open("users.json", 'r', encoding='utf-8') as f:
                                d = eval(f.read())
                            if (d[str(QQ_id)][1] < 0):
                                all = requests.get(where + 'get_group_member_list?group_id=' + str(grp_id))
                                sth = requests.get(where + 'get_group_info?group_id=' + str(grp_id))
                                if rd.randint(1, 10) <= 2:
                                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id,
                                                                                                    '[CQ:at,qq=' + str(
                                                                                                        QQ_id) + ']的现任老婆是[CQ:at,qq=' + str(
                                                                                                        all.json()[
                                                                                                            'data'][
                                                                                                            rd.randint(
                                                                                                                0,
                                                                                                                sth.json()[
                                                                                                                    'data'][
                                                                                                                    'member_count'] - 1)][
                                                                                                            'user_id']) + ']'))
                                else:
                                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id,
                                                                                                    '[CQ:at,qq=' + str(
                                                                                                        QQ_id) + ']你 没房没车 存款不到114514 怎么这么普信（bushi'))
                                qqy_dict[str(QQ_id)] = 1
                            else:
                                all = requests.get(where + 'get_group_member_list?group_id=' + str(grp_id))
                                sth = requests.get(where + 'get_group_info?group_id=' + str(grp_id))
                                if rd.randint(1, 10) <= 5:
                                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id,
                                                                                                    '[CQ:at,qq=' + str(
                                                                                                        QQ_id) + ']的现任老婆是[CQ:at,qq=' + str(
                                                                                                        all.json()[
                                                                                                            'data'][
                                                                                                            rd.randint(
                                                                                                                0,
                                                                                                                sth.json()[
                                                                                                                    'data'][
                                                                                                                    'member_count'] - 1)][
                                                                                                            'user_id']) + ']'))
                                else:
                                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id,
                                                                                                    '[CQ:at,qq=' + str(
                                                                                                        QQ_id) + ']你 没房没车 存款不到114514 怎么这么普信（bushi'))
                                qqy_dict[str(QQ_id)] = 1
                        else:
                            all = requests.get(where+'get_group_member_list?group_id='+str(grp_id))
                            sth = requests.get(where+'get_group_info?group_id='+str(grp_id))
                            if rd.randint(1,10)<=5:
                                requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'[CQ:at,qq='+str(QQ_id)+']的现任老婆是[CQ:at,qq='+str(all.json()['data'][rd.randint(0,sth.json()['data']['member_count']-1)]['user_id'])+']'))
                            else:
                                requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'[CQ:at,qq='+str(QQ_id)+']你 没房没车 存款不到114514 怎么这么普信（bushi'))
                            qqy_dict[str(QQ_id)]=1
                elif(Message.count('[CQ:at,qq=2813332482]') and Message.count('石蜡') and grp_id==587827174):
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'捏也石蜡qwq[CQ:at,qq='+str(QQ_id)+']'))
                    requests.get(where+'set_group_ban?group_id=%s&user_id=%s&duration=180'%(grp_id,str(QQ_id)))
                elif(Message=='闹离婚'):
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'离婚成功！\n话说你想不想当个大猛公1'))
                elif(Message.count('[CQ:at,qq=2813332482]') and (Message.count('超市') or Message.count('橄榄') or Message.count('铜丝') or Message.count('撅')) and grp_id==587827174):
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'那我来撅你60s罢（bushi'))
                    requests.get(where+'set_group_ban?group_id=%s&user_id=%s&duration=60'%(grp_id,str(QQ_id)))
                elif(Message.count('[CQ:at,qq=2813332482]') and Message.count('娶')):
                    if(rd.randint(1,10)==1):
                        requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'emmm……明奈酱心动了呢 >__<'))
                    else:
                        requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'强迫婚姻……貌似不太好的呢qwq'))
                elif(Message.count('[CQ:at,qq=2813332482]') and Message.count("可爱捏")):
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'捏！>__<'))
                elif(Message[0:5]=='天气查询 '):
                    try:
                        rsp = requests.get("https://api.seniverse.com/v3/weather/daily.json?key=STjgNT5b6ZCvjm-wW&location="+Message[5:]+"&language=zh-Hans&unit=c&start=0&days=1").json()['results'][0]['daily'][0]
                        msg = Message[5:]+"\n"+rsp['text_day']+'\n'+rsp['low']+"~"+rsp['high']+'℃'
                    except:
                        msg = '请正确填写城市名称，非中国大陆境内的城市无效'
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
                elif(Message[0:5]=='疫情查询 '):
                    try:
                        rsp = requests.get("https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province="+Message[5:].split(" ")[0]+"&city="+Message[5:].split(" ")[1],headers=hdrs).json()['data'][-1]
                        msg = Message[5:]+"\n新增无症状 "+str(rsp['yes_wzz_add'])+'\n新增确诊 '+str(rsp['yes_confirm_add'])+"\n累计确诊 "+str(rsp['confirm'])+'\n数据仅供参考'
                    except:
                        msg = '请正确填写省份/自治区/直辖市与城市/盟/自治州/直辖市的区县等等，中间要带有空格。'
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
                elif(Message[0:3]=='百度 '):
                    try:
                        msg = findbd.spider(findbd.search(Message[3:]))[5]
                        msg = msg[0:400]+'…\n详情请见\n'+findbd.search(Message[3:])
                    except:
                        msg = '没有找到结果'
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
                elif(Message[0:3]=='B站 '):
                    if(len(event_queue1)>len(event_queue2)):
                        requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'明奈酱已经把它加入下载队列了呢！请耐心等待前面的视频下载完成哦~\n你是第%s个下载视频的呢~'%(len(event_queue2)+1)))
                        event_queue2.append([grp_id,Message[3:],QQ_id])
                    else:
                        requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,'明奈酱已经把它加入下载队列了呢！请耐心等待前面的视频下载完成哦~\n你是第%s个下载视频的呢~'%(len(event_queue1)+1)))
                        event_queue1.append([grp_id,Message[3:],QQ_id])
                    if(not is_downloading1):
                        is_downloading1 = True
                        while(len(event_queue1)):
                            dld_id = event_queue1[0][0]
                            avbv = event_queue1[0][1]
                            idid = event_queue1[0][2]
                            del event_queue1[0]
                            try:
                                file_path = bili.download(avbv,1)
                                file_path = "/".join(os.getcwd().split('\\'))+"/"+file_path
                                requests.get(where+'upload_group_file?group_id=%s&file=%s&name=%s'%(dld_id,file_path,avbv+'.mp4'))
                                msg = '[CQ:at,qq='+str(idid)+']明奈酱下载完成辣！文件在群文件根目录内哦~名字就是av号或者bv号啦~\n使用明奈酱下载视频代表你同意你自己承担侵权的责任呢~'
                            except:
                                msg = '[CQ:at,qq='+str(idid)+']非常抱歉，明奈酱下载'+avbv+'失败了qwq\n可能是同时下载的视频太多啦\n可能我吃不下这么大的视频呀\n可能是视频本身有问题的呢啊\n可能是B站这个视频不存在啦啊'
                            requests.get(where+'send_group_msg?group_id=%s&message=%s'%(dld_id,msg))
                            try:
                                bili.ok(1)
                            except:
                                pass
                        is_downloading1 = False
                    elif(not is_downloading2):
                        is_downloading2 = True
                        while(len(event_queue2)):
                            dld_id = event_queue2[0][0]
                            avbv = event_queue2[0][1]
                            idid = event_queue2[0][2]
                            del event_queue2[0]
                            try:
                                file_path = bili.download(avbv,2)
                                file_path = "/".join(os.getcwd().split('\\'))+"/"+file_path
                                requests.get(where+'upload_group_file?group_id=%s&file=%s&name=%s'%(dld_id,file_path,avbv+'.mp4'))
                                msg = '[CQ:at,qq='+str(idid)+']明奈酱下载完成辣！文件在群文件根目录内哦~名字就是av号或者bv号啦~\n使用明奈酱下载视频代表你同意你自己承担侵权的责任呢~'
                            except:
                                msg = '[CQ:at,qq='+str(idid)+']非常抱歉，明奈酱下载'+avbv+'失败了qwq\n可能是同时下载的视频太多啦\n可能我吃不下这么大的视频呀\n可能是视频本身有问题的呢啊'
                            requests.get(where+'send_group_msg?group_id=%s&message=%s'%(dld_id,msg))
                            try:
                                bili.ok(2)
                            except:
                                pass
                        is_downloading2 = False
                elif(Message[:5]=='单词查询 '):
                    url = "https://fanyi.baidu.com/sug"
                    data = {
                        "kw": Message[5:]
                    }
                    resp = requests.post(url, data=data)
                    data_list = resp.json()['data']
                    msgl = []
                    for item in data_list:
                        cl = item['k']+":"+item['v']
                        msgl.append(cl)
                    msg = "\n".join(msgl)
                    msg = "%3b".join(msg.split(';'))
                    if(msg==''):
                        msg = '没有查到诶……'
                    else:
                        msg += '\n拿起单词本记下来嗷'
                    requests.get(where+'send_group_msg?group_id=%s&message='%(grp_id)+msg)
                elif(Message[:4]=='说句话 '):
                    send = Message[4:]
                    msg = '[CQ:tts,text=' + send[:220] + ']'
                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id, msg))
                    send = send[220:]
                    while(len(send)>220):
                        msg = '[CQ:tts,text='+send[:220]+']'
                        requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
                        send = send[220:]
                    msg = '使用明奈酱生成语音代表您同意明奈酱生成的语音没有任何法律效力，不一定具有真实性。'
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
                elif(Message[:13]=='Python Shell:'):
                    msg = pts.run(Message[13:])
                    requests.get(where + 'send_group_msg?group_id=%s&message=%s' % (grp_id, msg))
                elif(Message.count('[CQ:at,qq=2813332482]') and (Message.count('菜单'))):
                    msg = """明奈酱功能一览表~
========版本:1.6正式版=======
1.娶群友/签到
直接发送娶群友或者签到~
为防止打扰，一天只能爱一个人嗷~
签到代表你已经出家，戒掉了七情六欲，每日会有功德

2.疫情查询
国内才能查询嗷~
举个栗子√
疫情查询 宁夏 银川
疫情查询 内蒙古 阿拉善盟
疫情查询 北京 东城
疫情查询 浙江 温州 江南皮革厂（划

3.天气查询
这个比较宽松啦~
国内城市才能查嗷
天气查询 银川
天气查询 宁夏回族自治区 银川
天气查询 yinchuan
以上均可~

4.百度
百度 关键词
给你找百度百科~

5.B站
B站 av/bv号
下载视频，上传群文件~

6.定制功能
群主进群757767647来办理嗷
经过审核即可办理啦~

7.单词查询
单词查询 英语
给你说说这个单词啥意思

8.说句话
说句话 文本
文本转语音（明奈的声音可好听了呢）
【注意：本音频不能作为法律依据，造成纠纷后果自负】

9.Python Shell
Python Shell:Python代码
执行Python代码并发送该函数返回值（暂不开放）
"""
                    requests.get(where+'send_group_msg?group_id=%s&message=%s'%(grp_id,msg))
            else:
                msg = '''私聊功能已不开放。'''
                requests.get(where+'send_private_msg?user_id=%s&message=%s'%(QQ_id,msg))
    return 'OK'

app.run(debug=True, host='127.0.0.2', port=5701)
