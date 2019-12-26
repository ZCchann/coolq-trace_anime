import cqp
import requests
import json

def tra_anime(trace_url,eval_cqp_data):   #私聊 搜索番剧截图
    response = requests.get(trace_url)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    name = result["docs"][0]["title_chinese"]  # 切片番剧名称
    similarity = result["docs"][0]["similarity"]  # 切片相似度
    try:
        decimal = "." + str(similarity * 100).split('.')[1][:2]  # 切片小数点后的内容 如果为空则不返回
    except IndexError:
        decimal = ""

    time = result["docs"][0]["at"]  # 切片时间
    episode = result["docs"][0]["episode"]  # 切片集数
    search_results = {
        "user_id": eval_cqp_data['user_id'],
        "message": "番剧名称：" + name + " 第" + str(episode) + "集" + '\n' +
                    "相似度：" + str(similarity * 100).split('.')[0] + decimal + "%" + '\n' +
                    "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
    }
    return search_results

def group_tra_anime(trace_url,eval_cqp_data):   #群聊 搜索番剧截图
    response = requests.get(trace_url)  # 获取trace.moe的返回信息
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
    similarity = result["docs"][0]["similarity"]  # 切片相似度
    try:
        decimal = "." + str(similarity * 100).split('.')[1][:2]  # 切片小数点后的内容 如果为空则不返回
    except IndexError:
        decimal = ""
    time = result["docs"][0]["at"]  # 切片时间
    episode = result["docs"][0]["episode"]  # 切片集数
    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +'\n' +
                   "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                   "相似度：" + str(similarity * 100).split('.')[0] + decimal + "%" + '\n' +
                   "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
    }
    return search_results