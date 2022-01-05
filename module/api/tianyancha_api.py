import json
import os
import sys
import time
import random
from conf.log import logger
from bs4 import BeautifulSoup
import requests
from conf import config
from module import globals
from module.colors import color
from conf import config
from module import globals
from conf.log import logger
import time
from module import gadgets
import subprocess
import os
import json

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH = os.path.join(globals.get_value("RESULT_PATH"), "tianyancha")
if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)
RESULTS = []
TIANYANCHA_HEADERS=globals.get_value("TIANYANCHA_HEADERS")



class Tinayancha_Api:
    def get_url(self, url):
        urls = []
        rep = requests.get(url, headers=TIANYANCHA_HEADERS)
        soup = BeautifulSoup(rep.text, "lxml")
        trs = soup.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 0:
                continue
            urls.append(tds[1].a.get("href"))
        return urls

    def detail_write(self, detali):
        tmp_datail = {}
        tmp_datail["主办单位名称"] = detali["主办单位名称"]
        tmp_datail["主办单位性质"] = detali["主办单位性质"]
        try:
            tmp_datail["备案号"] = detali["备案号"]
            tmp_datail["域名"] = detali["域名"]
            tmp_datail["备案时间"] = detali["备案时间"]
        except:
            tmp_datail["备案号"] = detali["网站备案/许可号"]
            tmp_datail["域名"] = detali["网站域名"]
            tmp_datail["备案时间"] = detali["审核时间"]
        global RESULTS
        RESULTS.append(tmp_datail)
        print(color.green("[INFO]爬取到如下数据:"),json.dumps(tmp_datail,ensure_ascii=False))

    def get_detail(self, url):
        rep = requests.get(url, headers=TIANYANCHA_HEADERS)
        print(color.green("[INFO]正在爬取如下链接"),url)
        soup = BeautifulSoup(rep.text, "lxml")
        tables = soup.find_all("table")
        if len(tables) == 3 or len(tables) == 1:
            company = {}
            key = ""
            value = ""
            i = 0
            for td in tables[0].find_all("td"):
                if i % 2 == 0:
                    key = td.text
                else:
                    value = td.text
                i += 1
                company[key] = value
            self.detail_write(company)
        elif len(tables) == 0:
            if "我们只是确认一下你不是机器人" in rep.text:
                input(f"触发反爬机制，请打开链接手动确认下，确认结束后按任意键继续执行。{url}")
                self.get_detail(url)
            else:
                logger.warning(f"{color.red_warn()}{url}获取失败，请点击自行查看。")
        else:
            company = {}
            key = ""
            value = ""
            i = 0
            for td in tables[0].find_all("td"):
                if i % 2 == 0:
                    key = td.text
                else:
                    value = td.text
                i += 1
                company[key] = value
            for tr in tables[1].find_all("tr"):
                tmp_company = company
                tds = tr.find_all("td")
                if len(tds) == 0:
                    continue
                tmp_company["备案号"] = tds[1].text
                tmp_company["域名"] = tds[3].text
                tmp_company["备案时间"] = tds[4].text
                self.detail_write(tmp_company)

    def get_max_page(self, keyword):
        url = f"https://beian.tianyancha.com:443/search/{keyword}/p250"
        rep = requests.get(url, headers=TIANYANCHA_HEADERS)
        if "我们只是确认一下你不是机器人" in rep.text:
            logger.warning("触发反爬机制，请打开链接手动确认下，确认结束后按任意键继续执行:" + url)
            input()
            return self.get_max_page(keyword)
        elif "登录后查看更多信息" in rep.text:
            logger.error("天眼查cookie失效，请更新cookie'")
            sys.exit()
        else:
            try:
                soup = BeautifulSoup(rep.text, "lxml")
                return soup.find_all("li")[-1].a.text
            except:
                return 1

    def search_file_clean(self,  file):
        results = []
        domains = []
        with open(file, 'r', encoding="utf-8") as fp:
            tmp_results = json.load(fp)
        for result in tmp_results:
            domain = result['域名']
            if domain not in domains:
                results.append(result)
        with open(file, 'w', encoding="utf-8") as fp:
            json.dump(results, fp)


    def search_keyword(self, keyword,filepath):
        global RESULTS
        max_page = self.get_max_page(keyword)
        logger.info(f"关键词{keyword}共计有{max_page}页。")
        for i in range(int(max_page)):
            logger.info(f"{color.yel_info()}正在爬取关键词{keyword}第{i + 1}页，目前还剩余{int(max_page) - i - 1}页待爬取。")
            url = f"https://beian.tianyancha.com:443/search/{keyword}/p{i + 1}"
            for url in self.get_url(url):
                self.get_detail(url)
        with open(filepath,"w",encoding="utf-8") as fp:
            json.dump(RESULTS,fp,indent=4, ensure_ascii=False)
        self.search_file_clean(filepath)


tianyancha=Tinayancha_Api()
