import json

import requests
from PIL import Image
from urllib import request

class WxPusher(object):
    def __init__(self):
        self.tag = "WxPusher"
        self.app_token = "AT_eJUnwdE5oChckC0dGSc33n4eaz6CG7kU"
        self.user_ids = ["UID_dZS13V9mgIFOyvQpIe3u7D91mtct","UID_JkB2piJ4Gh2PQS5mzZ1YVz0ZbTJm"]
        self.send_url = "http://wxpusher.zjiecode.com/api/send/message"
        self.query_url = "http://wxpusher.zjiecode.com/api/send/query/{}"
        self.qrcode_url = "http://wxpusher.zjiecode.com/api/fun/create/qrcode"
        self.query_user_url = "http://wxpusher.zjiecode.com/api/fun/wxuser/v2"

        self.common_params = {
            "appToken":self.app_token,
            "contentType":1,
            "uids":self.user_ids,
        }
        self.headers = {
            'Content-Type':'application/json; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': 'wxpusher.zjiecode.com'

        }

    def log(self, content):
        print(self.tag,content)


    def send_msg(self,msg):
        data = self.common_params
        data["content"] = msg
        self.log(data)
        data = json.dumps(data)
        response = requests.post(self.send_url,data,headers=self.headers)
        self.log(response.text)
        return response.json()



    def query_msg(self,msg_id):
        url = self.query_url.format(msg_id)
        response = requests.get(url)
        self.log(response.text)
        return response.json()


    def get_qrcode(self):
        params = {
            "appToken":self.app_token,
            "extra":"py_push"
        }
        params = json.dumps(params)
        result = requests.post(self.qrcode_url,params,headers=self.headers)
        self.log(result.text)
        return result.json()

    def query_all_user(self):
        params = {
            "appToken":self.app_token,
            "page":1,
            "pageSize":100
        }
        result = requests.get(self.query_user_url,params)
        self.log(result.text)
        return result.json()

    def download_pic(self,img_url):
        result = request.urlopen(img_url)
        if result.getcode() == 200:
            with open("qr_code.jpg", "wb") as f:
                f.write(result.read())
                self.log("下载图片成功")
                return True

    def open_img(self,name):
        img = Image.open(name)
        img.show()
        self.log("显示二维码图片")

# http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_eJUnwdE5oChckC0dGSc33n4eaz6CG7kU&content=hello&uid=UID_dZS13V9mgIFOyvQpIe3u7D91mtct
if __name__ == '__main__':
    pusher = WxPusher()
    pusher.log("start")
    # response = pusher.send_msg("hello")
    # code = response['code']
    # pusher.log("发送消息返回码：{}".format(code))
    # if code == 1000:
    #     data_list = response['data']
    #     for data in data_list:
    #         pusher.query_msg(data['messageId'])

    # qr_code_data = pusher.get_qrcode()
    # if qr_code_data['code'] == 1000:
    #     data = qr_code_data['data']
    #     img_url = data['shortUrl']
    #     if pusher.download_pic(img_url):
    #         pusher.open_img("qr_code.jpg")

    # pusher.query_all_user()