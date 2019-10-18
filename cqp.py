# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify
import requests
import json

app = Flask(__name__)
siliao = 'http://127.0.0.1:5700/send_private_msg?' #酷Q http插件私聊推送url
qunliao = 'http://127.0.0.1:5700/send_group_msg?' #酷Q http插件群聊推送url
trace_moe_url = 'https://trace.moe/api/search?url='  #trace.moe的api地址
user_private_list = []  #暂存发送者QQ号的列表
user_group_list = [] #暂存群搜图 群号

@app.route('/',methods=[ 'POST'])
def tarce_amine():
    cqp_push_data = request.get_data()  #获取机器人推送的内容
    zhuanhuan = cqp_push_data.decode('utf-8')  #转换utf-8编码
    eval_cqp_data = json.loads(zhuanhuan) #转换推送内容为字典格式
    private_number = 0
    group_number = 0
#####################################私聊 只发文字 后发图###################################################################
    if eval_cqp_data['message_type'] == 'private':
        if eval_cqp_data['message'] == '识别番剧截图':  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in user_private_list:
                user_private_list.append(eval_cqp_data['user_id'])
                search_results = {
                    "user_id": eval_cqp_data['user_id'],
                    "message": '请发送图片'
                }
                requests.get(url=siliao, params=search_results)

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in user_private_list:
                if eval_cqp_data['user_id'] == c:
                    message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
                    trace_url = trace_moe_url + message_url
                    kaifuku = {
                        "user_id": eval_cqp_data['user_id'],
                        "message": "番剧截图识别中 请稍后......"
                    }
                    requests.get(url=siliao , params=kaifuku)
                    response = requests.get(trace_url)  # 获取trace.moe的返回信息
                    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
                    result = response.json()  # 转换成json格式
                    animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
                    similarity = result["docs"][0]["similarity"]  # 切片相似度
                    time = result["docs"][0]["at"]  # 切片时间
                    episode = result["docs"][0]["episode"]  # 切片集数
                    search_results = {
                        "user_id": eval_cqp_data['user_id'],
                        "message": "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                                   "相似度：" + str(similarity * 100).split('.')[0] + "." + str(similarity * 100).split('.')[1][
                                                                                        :2] + "%"
                                   + '\n' + "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
                    }
                    requests.get(url=siliao, params=search_results)
                    user_private_list.pop(private_number)
                    break
                private_number = private_number + 1
 #######################################################################################################################

#####################################私聊 发文字带图片###################################################################
        elif "识别番剧截图" in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]   #切片内容 把图片的url切片出来
            trace_url=trace_moe_url + message_url
            kaifuku = {
                "user_id": eval_cqp_data['user_id'],
                "message": "番剧截图识别中 请稍后......"
            }
            requests.get(url = siliao,params=kaifuku)
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
            requests.get(url = siliao,params=search_results)
######################################################################################################################

#####################################群聊 只发文字 后发图###################################################################
    if eval_cqp_data['message_type'] == 'group':
        if eval_cqp_data['message'] == '识别番剧截图':  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in user_group_list:
                group_number_list.append(eval_cqp_data['user_id'])
                search_results = {
                    "group_id": eval_cqp_data['group_id'],
                    "message": '请发送图片'
                }
                requests.get(url=qunliao, params=search_results)


        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in user_group_list:
                if eval_cqp_data['user_id'] == c:
                    message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[
                        1]  # 切片内容 把图片的url切片出来
                    trace_url = trace_moe_url + message_url
                    kaifuku = {
                        "group_id": eval_cqp_data['group_id'],
                        "message": "番剧截图识别中 请稍后......"
                    }
                    requests.get(url=qunliao, params=kaifuku)
                    response = requests.get(trace_url)  # 获取trace.moe的返回信息
                    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
                    result = response.json()  # 转换成json格式
                    animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
                    similarity = result["docs"][0]["similarity"]  # 切片相似度
                    time = result["docs"][0]["at"]  # 切片时间
                    episode = result["docs"][0]["episode"]  # 切片集数
                    search_results = {
                        "group_id": eval_cqp_data['group_id'],
                        "message": "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                                   "相似度：" + str(similarity * 100).split('.')[0] + "." +
                                   str(similarity * 100).split('.')[1][
                                   :2] + "%"
                                   + '\n' + "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[
                                       0] + '秒'
                    }
                    requests.get(url=qunliao, params=search_results)
                    group_number_list.pop(group_number)
                    break
                group_number = group_number + 1
#######################################################################################################################

#####################################群聊 发文字带图片###################################################################
        elif "识别番剧截图"  in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            trace_url = trace_moe_url + message_url
            kaifuku = {
                "group_id": eval_cqp_data['group_id'],
                "message": "番剧截图识别中 请稍后......"
            }
            requests.get(url=qunliao, params=kaifuku)
            response = requests.get(trace_url)  # 获取trace.moe的返回信息
            response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
            result = response.json()  # 转换成json格式
            animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
            similarity = result["docs"][0]["similarity"]  # 切片相似度
            time = result["docs"][0]["at"]  # 切片时间
            episode = result["docs"][0]["episode"]  # 切片集数
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                           "相似度：" + str(similarity * 100).split('.')[0] + "." + str(similarity * 100).split('.')[1][
                                                                                :2] + "%"
                           + '\n' + "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
            }
            requests.get(url=qunliao, params=search_results)
######################################################################################################################
    return (cqp_push_data)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port='5000')