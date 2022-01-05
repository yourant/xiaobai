# coding:utf-8
from conf.log import logger
from module import globals
import requests
import json
import math

import re

class QuakeApi:
    def __init__(self, key):
        self.MaxTotal = 10000
        self.TIMEMOUT = 1000
        self.X_QuakeToken = key

    def query_domain(self, query_str):
        print('[quake] 查询：{}'.format(query_str))
        return self.query(query_str)

    def query_ip(self, query_str):
        logger.info('[quake] 查询：{}'.format(query_str))
        return self.query(query_str)

    def filter_data(self, data):
        quake_Results_tmp = []
        for each_data in data:
            '''host	标题	ip	子域名	端口	服务	协议	地址	查询语句	robots'''
            ip, port, host, name, title, path, product, province_cn, favicon, x_powered_by, cert = '', '', '', '', '', '', '', '', '', '', ''

            ip = each_data['ip']  # ip
            port = each_data['port']  # port
            location = each_data['location']  # 地址
            service = each_data['service']

            province_cn = location['province_cn']  # 地址

            name = service['name']  # 协议
            product = service['product']  # 服务
            if 'cert' in service.keys():
                cert = service['cert']  # 证书
                cert = re.findall("DNS:(.*?)\n", cert)

            if 'http' in service.keys():
                http = service['http']
                host = http['host']  # 子域名
                title = http['title']  # title

            host, title, ip, subdomain, port, server, protocol, address, cert = host, title, ip, host, port, product, name, province_cn, cert
            quake_Result = [host, title, ip, subdomain, port, server, protocol, address, cert]
            quake_Results_tmp.append(quake_Result)

        return quake_Results_tmp

    def query(self, query_str,size):
        quake_Results = []
        quake_web_host_port = []
        quake_service_host_port = []
        headers = {
            "X-QuakeToken": self.X_QuakeToken
        }
        data = {
            "query": query_str,
            "start": 0,
            "size": size
        }
        # 查询剩余积分
        try:
            response = requests.get(url="https://quake.360.cn/api/v3/user/info", headers=headers, json=data,
                                    timeout=self.TIMEMOUT)
            month_remaining_credit = response.json()["data"]["month_remaining_credit"]
            logger.info('[quake] 积分剩余:{}'.format(month_remaining_credit))
        except Exception as e:
            logger.error('[quake] api error')
            return [], [], []

        # 查询
        try:
            response = requests.post(url="https://quake.360.cn/api/v3/search/quake_service", headers=headers, json=data,
                                     timeout=self.TIMEMOUT)
        except Exception as e:
            logger.error('[quake] error: {}'.format(e.args))
            return [], [], []

        if response.status_code != 200:
            logger.error('[quake] api error')
            return [], [], []

        ret = response.json()
        # print(ret)

        if ret['meta'] == {}:
            print(ret['message'])
            return [], [], []

        meta = ret['meta']
        data = ret['data']

        total = meta['pagination']["total"]
        count = meta['pagination']['count']
        if total == 0:
            return [], [], []
        logger.info('[quake] 总共数据量:{}'.format(total))
        total = self.MaxTotal if total > self.MaxTotal else total
        pages = total / count
        pages = math.ceil(pages)
        logger.info('[quake] 限定查询的数量:{}'.format(total))
        logger.info('[quake] 查询的页数:{}'.format(pages))

        logger.info("[quake] page{}".format(1))
        quake_Results_tmp = self.filter_data(data)
        quake_Results.extend(quake_Results_tmp)
        return quake_Results[0]

QUAKE_KEY=globals.get_value("QUAKE_KEY")
qk = QuakeApi(key=QUAKE_KEY)
