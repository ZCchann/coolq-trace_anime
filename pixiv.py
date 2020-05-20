import requests
import json

def day_illust(eval_cqp_data):
    pixiv_date = requests.get("https://api.zcchann.top/api/v1/pixiv/day_illust").json()
    pixiv_url = ""
    for i in range(len(pixiv_date["image_url"])):
        pixiv_url += "[CQ:image,file=%s]"%(pixiv_date["image_url"][i])
    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": pixiv_url  # 返回图片的CQ码给酷Q air版无法发送图片
    }
    return json.dumps(search_results)
