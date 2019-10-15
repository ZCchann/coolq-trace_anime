# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify
import requests
import json

app = Flask(__name__)
@app.route('/',methods=[ 'POST'])
def data():
    cqp_push_data = request.get_data()  #获取机器人推送的内容
    zhuanhuan = cqp_push_data.decode('utf-8')  #转换utf-8编码
    eval_cqp_data = json.loads(zhuanhuan) #转换推送内容为字典格式
    if eval_cqp_data['message_type'] == 'private' and str(eval_cqp_data['message'].split('[')[0]).replace('\r\n','') == '识别番剧截图' : # 私聊搜索番剧截图  replace 删除换行符跟回车
        message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]   #切片内容 把图片的url切片出来
        push_url = 'https://trace.moe/api/search?url='  #trace.moe的api地址
        trace_url=push_url + message_url
        url = 'http://127.0.0.1:5700/send_private_msg?'   #酷Q机器人 http api 插件地址
        kaifuku = {
            "user_id": eval_cqp_data['user_id'],
            "message": "番剧截图识别中 请稍后......"
        }
        requests.get(url = url,params=kaifuku)
        response = requests.get(trace_url)  #获取trace.moe的返回信息
        response.encoding = 'utf-8'  #把trace.moe的返回信息转码成utf-8
        result = response.json()  #转换成json格式
        animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
        similarity = result["docs"][0]["similarity"]  # 切片相似度
        time = result["docs"][0]["at"]  # 切片时间
        episode = result["docs"][0]["episode"]  # 切片集数
        search_results = {
                "user_id": eval_cqp_data['user_id'],
                "message": "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                "相似度：" + str(similarity * 100).split('.')[0] + "." + str(similarity * 100).split('.')[1][:2] + "%"
                + '\n' + "时间：" + str(time / 60).split('.')[0] + '分'+ str(time % 60).split('.')[0] + '秒'
                }
        requests.get(url = url,params=search_results)
    elif eval_cqp_data['message_type'] == 'group' and str(eval_cqp_data['message'].split('[')[0]).replace('\r\n','') == '识别番剧截图' : #群聊识别番剧截图功能
        message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
        push_url = 'https://trace.moe/api/search?url='  # trace.moe的api地址
        trace_url = push_url + message_url
        url = 'http://127.0.0.1:5700/send_group_msg?'  # 酷Q机器人 http api 插件地址
        kaifuku = {
            "group_id": eval_cqp_data['group_id'],
            "message": "番剧截图识别中 请稍后......"
        }
        requests.get(url=url, params=kaifuku)
        response = requests.get(trace_url)  # 获取trace.moe的返回信息
        response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
        result = response.json()  # 转换成json格式
        animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
        similarity = result["docs"][0]["similarity"]  # 切片相似度
        time = result["docs"][0]["at"]  # 切片时间
        episode = result["docs"][0]["episode"]  # 切片集数
        search_results = {
            "group_id": eval_cqp_data['group_id'],
            "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" + '\n' +
                       "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                       "相似度：" + str(similarity * 100).split('.')[0] + "." + str(similarity * 100).split('.')[1][:2]
                       + "%" + '\n' + "时间：" + str(time / 60).split('.')[0] + '分'+ str(time % 60).split('.')[0] + '秒' ,
            # "auto_escape":"true"
        }
        requests.get(url=url, params=search_results)

    return (cqp_push_data)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port='5000')
