import requests
import json
import os
import base64
from module import globals
from conf.log import logger

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH = globals.get_value("RESULT_PATH")

if not os.path.exists(os.path.join(RESULT_PATH,"fofa")):
    os.makedirs(os.path.join(RESULT_PATH,"fofa"))

class FofaApi:

    def __init__(self, email, key):
        self.email = email
        self.key = key

    # 获取基础信息
    def get_me_info(self):
        api = f"https://fofa.so/api/v1/info/my?email={self.email}&key={self.key}"
        r_json = json.loads(requests.get(api).text)
        print("当前用户昵称：" + r_json['username'])
        print("当前用户头像：" + r_json['avatar'])
        print("当前用户邮箱：" + r_json['email'])
        print("Fofa版本：" + r_json['fofacli_ver'])
        return r_json

    # 搜索功能
    def get_search(self, search,fields="host,title,protocol,ip,port,domain,country_name,province,city", size=100):
        # 请求FofaAPI
        logger.info(f"正在使用FOFA搜索关键字{search}。")
        # num = int(int(size) / 100) + 1
        # for i in range(num):
        qbase64 = base64.b64encode(search.encode()).decode()
        api = f"https://fofa.so/api/v1/search/all?email={self.email}&key={self.key}&qbase64={qbase64}&size={size}&fields={fields}"
        try:
            r = requests.get(api)
            r_json = json.loads(r.text)
            # 判断错误信息
            if r_json['error']:
                if r_json['errmsg'] == "Internal Server Error!":
                    print("服务器错误")
                elif r_json['errmsg'] == "FOFA coin is not enough!":
                    print("Fofa币不足")
                elif r_json['errmsg'] == "Result window is too large, page must be less than or equal to...!":
                    print("结果窗口过大")
                elif r_json['errmsg'] == "limits must less than 10001":
                    print("超过API限制")
                elif r_json['errmsg'] == "401 Unauthorized, make sure email and apikey is correct.":
                    print("鉴权失败，请重新确认邮箱和API KEY")
                elif r_json['errmsg'] == '820103':
                    print("格式错误，请重新输入")
                elif r_json['errmsg'] =="Request overrun on the day, restrict access, try again tomorrow":
                    print("请求次数过多")
            else:
                return r_json["results"]
        except Exception as e:
            logger.error(api,e)
            return []



    def search_ip(self, search,output_file):
        results=[]
        result = self.get_search(search, size=10000)
        results.append(result)
        with open(output_file,"w",encoding="utf-8") as fp:
            json.dump(results,fp)


    def search_files(self,input_file,output_file):
        results=[]
        with open(input_file,'r',encoding="utf-8") as fp:
            json_results=fp.readlines()
        for json_result in json_results:
            result=self.get_search(json_result.strip(),size=10000)
            results.append(result)
        with open(output_file,"w",encoding="utf-8") as fp:
            json.dump(results,fp,ensure_ascii=False,indent=4)

FOFA_EMAIL = globals.get_value("FOFA_EMAIL")
FOFA_KEY = globals.get_value("FOFA_KEY")
# main
fofa=FofaApi(FOFA_EMAIL,FOFA_KEY)

