# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify
import requests
import json

def config_api_key():
    conf = open("config.json", encoding='utf-8')
    setting = json.load(conf)
    api_key = setting['api_key']
    return api_key

def config_tarce_message():
    conf = open("config.json", encoding='utf-8')
    setting = json.load(conf)
    tarce_message = setting['tarce_message']
    return tarce_message

def config_search_message():
    conf = open("config.json", encoding='utf-8')
    setting = json.load(conf)
    search_message = setting['search_message']
    return search_message

def config_coolq_http_api_ip():
    conf = open("config.json", encoding='utf-8')
    setting = json.load(conf)
    coolq_http_api_ip = setting['coolq_http_api_ip']
    return coolq_http_api_ip

def config_coolq_http_api_port():
    conf = open("config.json", encoding='utf-8')
    setting = json.load(conf)
    coolq_http_api_port = setting['coolq_http_api_port']
    return coolq_http_api_port

app = Flask(__name__)
siliao = 'http://'+ config_coolq_http_api_ip() + ':'+ config_coolq_http_api_port() +'/send_private_msg?' #酷Q http插件私聊推送url
qunliao = 'http://'+ config_coolq_http_api_ip() + ':'+ config_coolq_http_api_port() +'/send_group_msg?' #酷Q http插件群聊推送url
trace_moe_url = 'https://trace.moe/api/search?url='  #trace.moe的api地址
search_image_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&' #saucenao的API地址
api_key = config_api_key() #saucenao的api key
tarce_message = config_tarce_message() #搜番剧的命令
search_message = config_search_message() #搜图片的命令
user_private_list = []  #暂存 搜索番剧发送者QQ号的列表
user_group_list = [] #暂存搜索番剧 群搜图 群号
search_acg_image_list = [] #暂存 搜索图片发送者QQ号的列表
search_acg_image_group_list = []#暂存 搜索图片 群搜图的群号

@app.route('/',methods=[ 'POST'])
def tarce_amine():
    cqp_push_data = request.get_data()  #获取机器人推送的内容
    zhuanhuan = cqp_push_data.decode('utf-8')  #转换utf-8编码
    eval_cqp_data = json.loads(zhuanhuan) #转换推送内容为字典格式
    private_number = 0
    group_number = 0
    search_acg_number = 0
    search_acg_group_number = 0
#####################################私聊 只发文字 后发图 识别番剧####################################################
    if eval_cqp_data['message_type'] == 'private':
        if eval_cqp_data['message'] == tarce_message:  # 私聊搜索番剧截图  replace 删除换行符跟回车
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
#  #######################################################################################################################
#
# #####################################私聊 发文字带图片###################################################################
        elif tarce_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
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

#####################################群聊 只发文字 后发图 识别番剧####################################################
    if eval_cqp_data['message_type'] == 'group':
        if eval_cqp_data['message'] == tarce_message:  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in user_group_list:
                user_group_list.append(eval_cqp_data['user_id'])
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
                        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" + '\n' +
                                   "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                                   "相似度：" + str(similarity * 100).split('.')[0] + "." +
                                   str(similarity * 100).split('.')[1][
                                   :2] + "%"
                                   + '\n' + "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[
                                       0] + '秒'
                    }
                    requests.get(url=qunliao, params=search_results)
                    user_group_list.pop(group_number)
                    break
                group_number = group_number + 1
# #######################################################################################################################
#
# #####################################群聊 发文字带图片###################################################################
        elif tarce_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
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
                "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +'\n' +
                           "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                           "相似度：" + str(similarity * 100).split('.')[0] + "." +
                           str(similarity * 100).split('.')[1][:2] + "%"
                           + '\n' + "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
            }
            requests.get(url=qunliao, params=search_results)
######################################################################################################################

#####################################私聊 只发文字 后发图 搜索图片####################################################
    if eval_cqp_data['message_type'] == 'private':
        if eval_cqp_data['message'] == search_message:
            if eval_cqp_data['user_id'] not in search_acg_image_list: #如果发送命令的QQ号不存在user_private_list表当中
                search_acg_image_list.append(eval_cqp_data['user_id']) #将QQ号暂存至user_private_list表当中
                kaifuku = {
                    "user_id": eval_cqp_data['user_id'],
                    "message": '请发送图片'
                }
                requests.get(url=siliao, params=kaifuku)
        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in search_acg_image_list:
                if eval_cqp_data['user_id'] == c:
                    trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
                    search_image = search_image_url + 'api_key=' + api_key + '&url=' +trace_image_url
                    kaifuku = {
                        "user_id": eval_cqp_data['user_id'],
                        "message": "图片搜索中 请稍后......"
                    }
                    requests.get(url=siliao , params=kaifuku)
                    response = requests.get(search_image)  # 获取trace.moe的返回信息
                    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
                    result = response.json()  # 转换成json格式
                    pixiv_id = int(result['results'][0]['data']['pixiv_id'])
                    ext_urls = str(result['results'][0]['data']['ext_urls'])
                    similarity = result['results'][0]['header']['similarity']
                    member_name = result['results'][0]['data']['member_name']
                    title = result['results'][0]['data']['title']
                    mini_image = result['results'][0]['header']['thumbnail']

                    search_results = {
                        "user_id": eval_cqp_data['user_id'],
                        "message": "[CQ:image,file=" + str(mini_image) + "]" + '\n'+    #返回图片的CQ码给酷Q air版无法发送图片
                                   "相似度 " + str(similarity) +'%' + '\n' +
                                   "作者名称 " + str(member_name) + '\n'+
                                   "图片名称 "+ str(title) + '\n' +
                                   "P站id " + str(pixiv_id)+'\n' +
                                   "图片链接 " + '\n' + ext_urls.replace('[','').replace(']','').replace("'",'')
                        }
                    requests.get(url=siliao, params=search_results)
                    search_acg_image_list.pop(search_acg_number)
                    break
                search_acg_number = search_acg_number + 1
######################################私聊 发文字带图片 搜索图片###############################################################
        elif search_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
            kaifuku = {
                "user_id": eval_cqp_data['user_id'],
                "message": "图片搜索中 请稍后......"
            }
            requests.get(url=siliao, params=kaifuku)
            response = requests.get(search_image)  # 获取trace.moe的返回信息
            response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
            result = response.json()  # 转换成json格式
            pixiv_id = int(result['results'][0]['data']['pixiv_id'])
            ext_urls = str(result['results'][0]['data']['ext_urls'])
            similarity = result['results'][0]['header']['similarity']
            member_name = result['results'][0]['data']['member_name']
            title = result['results'][0]['data']['title']
            mini_image = result['results'][0]['header']['thumbnail']

            search_results = {
                "user_id": eval_cqp_data['user_id'],
                "message": "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                           "相似度 " + str(similarity) + '%' + '\n' +
                           "作者名称 " + str(member_name) + '\n' +
                           "图片名称 " + str(title) + '\n' +
                           "P站id " + str(pixiv_id) + '\n' +
                           "图片链接 " + '\n' + ext_urls.replace('[', '').replace(']', '').replace("'", '')
            }
            requests.get(url=siliao, params=search_results)

#####################################群聊 只发文字 后发图 识别番剧#############################
    if eval_cqp_data['message_type'] == 'group':
        if eval_cqp_data['message'] == search_message:  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in search_acg_image_group_list :
                search_acg_image_group_list .append(eval_cqp_data['user_id'])
                kaifuku = {
                    "group_id": eval_cqp_data['group_id'],
                    "message": "请发送图片"
                }
                requests.get(url=qunliao, params=kaifuku)

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in search_acg_image_group_list:
                if eval_cqp_data['user_id'] == c:
                    trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[
                        1]  # 切片内容 把图片的url切片出来
                    search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
                    kaifuku = {
                        "group_id": eval_cqp_data['group_id'],
                        "message": "图片搜索中 请稍后......"
                    }
                    requests.get(url=qunliao, params=kaifuku)
                    response = requests.get(search_image)  # 获取trace.moe的返回信息
                    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
                    result = response.json()  # 转换成json格式
                    pixiv_id = int(result['results'][0]['data']['pixiv_id'])
                    ext_urls = str(result['results'][0]['data']['ext_urls'])
                    similarity = result['results'][0]['header']['similarity']
                    member_name = result['results'][0]['data']['member_name']
                    title = result['results'][0]['data']['title']
                    mini_image = result['results'][0]['header']['thumbnail']
                    search_results = {
                        "group_id": eval_cqp_data['group_id'],
                        "message":"[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +
                                   "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                                   "相似度 " + str(similarity) + '%' + '\n' +
                                   "作者名称 " + str(member_name) + '\n' +
                                   "图片名称 " + str(title) + '\n' +
                                   "P站id " + str(pixiv_id) +'\n' +
                                   "图片链接 " + '\n' + str(ext_urls.replace('[', '').replace(']', '').replace("'", ''))
                    }
                    requests.get(url=qunliao, params=search_results)
                    search_acg_image_group_list.pop(search_acg_group_number)
                    break
                search_acg_group_number = search_acg_group_number + 1
        ###############################群聊 发文字带图片 搜索图片###################################
        elif  search_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
            kaifuku = {
                "group_id": eval_cqp_data['group_id'],
                "message": "图片搜索中 请稍后......"
            }
            requests.get(url=qunliao, params=kaifuku)
            response = requests.get(search_image)  # 获取trace.moe的返回信息
            response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
            result = response.json()  # 转换成json格式
            pixiv_id = int(result['results'][0]['data']['pixiv_id'])
            ext_urls = str(result['results'][0]['data']['ext_urls'])
            similarity = result['results'][0]['header']['similarity']
            member_name = result['results'][0]['data']['member_name']
            title = result['results'][0]['data']['title']
            mini_image = result['results'][0]['header']['thumbnail']
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" +
                           "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                           "相似度 " + str(similarity) + '%' + '\n' +
                           "作者名称 " + str(member_name) + '\n' +
                           "图片名称 " + str(title) + '\n' +
                           "P站id " + str(pixiv_id) + '\n' +
                           "图片链接 " + '\n' + str(ext_urls.replace('[', '').replace(']', '').replace("'", ''))
            }
            requests.get(url=qunliao, params=search_results)

    return (cqp_push_data)



if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port='5000')