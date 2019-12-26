import requests
import cqp
import json

def tra_images(images_url,eval_cqp_data):
    response = requests.get(images_url)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    try:
        mini_image = result['results'][0]['header']['thumbnail']  # 缩略图
    except KeyError:
        mini_image = ""
    try:
        similarity = result['results'][0]['header']['similarity']  # 相似度
    except KeyError:
        similarity = ""
    try:
        jp_name = result['results'][0]['data']['jp_name']
    except KeyError:
        jp_name = ""
    try:
        ext_urls = result['results'][0]['data']['ext_urls'][0]
    except KeyError:
        ext_urls = ""
    try:
        pixiv_id = int(result['results'][0]['data']['pixiv_id'])
    except KeyError:
        pixiv_id = ""
    try:
        member_name = result['results'][0]['data']['member_name']
    except KeyError:
        member_name = ""
    try:
        title = result['results'][0]['data']['title']
    except KeyError:
        title = ""
    search_results = {
        "user_id": eval_cqp_data['user_id'],
        "message": "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                   "相似度 " + str(similarity) + '%' + '\n' +
                   "作者名称 " + str(member_name) + '\n' +
                   "图片名称 " + str(title) + '' + jp_name + '\n' +
                   "P站id " + str(pixiv_id) + '\n' +
                   "图片链接 " + '\n' + ext_urls
    }
    return search_results


def tra_images_group(images_url,eval_cqp_data):
    response = requests.get(images_url)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    try:
        mini_image = result['results'][0]['header']['thumbnail']  # 缩略图
    except KeyError:
        mini_image = ""
    try:
        similarity = result['results'][0]['header']['similarity']  # 相似度
    except KeyError:
        similarity = ""
    try:
        jp_name = result['results'][0]['data']['jp_name']
    except KeyError:
        jp_name = ""
    try:
        ext_urls = result['results'][0]['data']['ext_urls'][0]
    except KeyError:
        ext_urls = ""
    try:
        pixiv_id = int(result['results'][0]['data']['pixiv_id'])
    except KeyError:
        pixiv_id = ""
    try:
        member_name = result['results'][0]['data']['member_name']
    except KeyError:
        member_name = ""
    try:
        title = result['results'][0]['data']['title']
    except KeyError:
        title = ""
    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" +
                   "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                   "相似度 " + str(similarity) + '%' + '\n' +
                   "作者名称 " + str(member_name) + '\n' +
                   "图片名称 " + str(title) + '' + jp_name + '\n'
                                                         "P站id " + str(pixiv_id) + '\n' +
                   "图片链接 " + '\n' + str(ext_urls.replace('[', '').replace(']', '').replace("'", ''))
    }
    return search_results