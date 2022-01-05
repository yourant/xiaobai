# encoding:utf-8
import zoomeye.sdk as zoomeye
import requests
import json
import os
import argparse
import base64
from prettytable import PrettyTable
import time
from module import globals
from conf.log import logger
ZOOMEYE_API_KEY=globals.get_value("ZOOMEYE_API_KEY")
class ZoomApi:

    def __init__(self,api_key):
        self.api_key=api_key
        self.zm = zoomeye.ZoomEye(api_key=self.api_key)

    # 验证API KEY

    def zoom_search(self,network):
        print(self.zm.resources_info()["quota_info"]["remain_free_quota"])
        data = self.zm.dork_search(network)
        # zoomeye.show_site_ip(data)
        return self.zm.dork_filter("ip,port,service")
        # # print(data1)

zoomeyeapi=ZoomApi(ZOOMEYE_API_KEY)


