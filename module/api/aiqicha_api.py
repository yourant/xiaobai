import re
import requests
import json
import urllib3
from conf import config
from module import globals
from conf.log import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers=globals.get_value("AIQICHA_HEADERS")


requests_proxies = None

# 网站备案的细节
icpinfo_url = "https://aiqicha.baidu.com/detail/icpinfoajax?p=1&size=20&pid=111111111111"
# 对外投资的细节
invest_url = "https://aiqicha.baidu.com/detail/investajax?p=1&size=20&pid=111111111111"
# 控股企业的细节
hold_url = "https://aiqicha.baidu.com/detail/holdajax?p=1&size=20&pid=111111111111"
# 分支机构的细节
branch_url = "https://aiqicha.baidu.com/detail/branchajax?p=1&size=20&pid=111111111111"

# 每页的条数
size = 10
# 超时
TIMEOUT = 20

invest_infos = []
holds_infos = []
branch_infos = []


# 获取基本信息:公司名、邮箱地址、联系方式
def companyDetail(pid):
    companyDetail_infos = {"emails": "", "telephone": ""}
    try:
        url = "https://aiqicha.baidu.com/company_detail_{}".format(pid)
        res = requests.get(url=url, headers=headers, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
        text = res.text
        # print(text)
        # companyName = re.findall('entName":"(.*?)"', text)[0].encode('utf-8').decode('unicode_escape')
        emails = re.findall(r'email":"(.*?)"', text)
        telephone = re.findall('telephone":"(.*?)"', text)
        # print("公司名、邮箱地址、联系方式")
        # print(companyName[0].encode('utf-8').decode('unicode_escape'), emails, telephone)
        companyDetail_infos = {"emails": emails, "telephone": telephone}
    except Exception as e:
        # print(e.args)
        pass
    # print()
    return companyDetail_infos

# 网站备案信息
def icpinfo(pid, icpinfo_page):
    icpinfo_infos = []
    for i in range(1, icpinfo_page+1):
        try:
            invest_url = "https://aiqicha.baidu.com/detail/icpinfoajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=invest_url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
            text = res.text.encode('utf8').decode('unicode_escape')
            text = json.loads(text)
            data = text["data"]
            for each in data["list"]:
                siteName = each["siteName"]
                logger.info("收集网站【{}】的备案信息".format(siteName))
                domain = each["domain"]
                icpNo = each["icpNo"]
                icpinfo_infos.append({"siteName": siteName, "domain": domain, "icpNo": icpNo})
        except Exception as e:
            pass
    return icpinfo_infos

# 对外投资
def invest(pid, invest_page):
    logger.info("开始查询对外投资企业:{}".format(invest_num))
    for i in range(1, invest_page+1):
        try:
            invest_url = "https://aiqicha.baidu.com/detail/investajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=invest_url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            for each in data["list"]:
                # 对外投资企业名称
                entName = each["entName"]
                logger.info("查询对外投资企业【{}】".format(entName))
                # 投资占比
                regRate = each["regRate"]
                # 被投资企业的pid
                invest_pid = each["pid"]
                icpinfo_infos = icpinfo(invest_pid, 1)
                companyDetail_infos = companyDetail(invest_pid)
                invest_infos.append({"pid": invest_pid, "invest_info": {"entName": entName, "regRate": regRate}, "icp_info": icpinfo_infos, "companyDetail_infos": companyDetail_infos})
                # invest_info.append({invest_pid: [entName, regRate]})
        except Exception as e:
            pass

# 控股企业
def holds(pid, holds_page):
    logger.info("开始查询控股企业: {}".format(holds_num))
    for i in range(1, holds_page+1):
        try:
            holds_url = "https://aiqicha.baidu.com/detail/holdsajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=holds_url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            for each in data["list"]:
                # 控股企业名称
                entName = each["entName"]
                logger.info("查询控股企业【{}】".format(entName))
                # 投资占比
                proportion = each["proportion"]
                # 控股企业pid
                holds_pid = each["pid"]
                # print(entName, proportion, holds_pid)
                icpinfo_infos = icpinfo(holds_pid, 1)
                companyDetail_infos = companyDetail(holds_pid)
                holds_infos.append({"pid": holds_pid, "holds_info": {"entName": entName, "proportion": proportion},  "icp_info": icpinfo_infos, "companyDetail_infos": companyDetail_infos})
        except Exception as e:
            print(e.args)
    print()

# 分支机构
def branch(pid, branch_page):
    logger.info("开始查询分支机构:{} ".format(branch_num))
    for i in range(1, branch_page + 1):
        try:
            branch_url = "https://aiqicha.baidu.com/detail/branchajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=branch_url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            # print(data)
            # print("分支机构名称、分支机构pid")
            for each in data["list"]:
                # print(each)
                # 分支机构名称
                entName = each["entName"]
                logger.info("查询分支机构【{}】".format(entName))
                # 控股企业pid
                branch_pid = each["pid"]
                # print(entName, branch_pid)
                icpinfo_infos = icpinfo(branch_pid, 1)
                companyDetail_infos = companyDetail(branch_pid)
                branch_infos.append({"pid": branch_pid, "branch_info": {"entName": entName},  "icp_info": icpinfo_infos, "companyDetail_infos": companyDetail_infos})
        except Exception as e:
            print(e.args)




def start(searchContent):
    # 获取匹配度最高的pid
    url = 'https://aiqicha.baidu.com/s?q={}&t=0'.format(searchContent)
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=TIMEOUT)
    except Exception as e:
        print(e)
        return [], [], [], []
    text = res.text
    # queryStr = re.findall('queryStr":"(.*?)"', text)
    # 取第一个pid，是匹配度最高的
    pids = re.findall('pid":"(.*?)"', text)
    if pids == []:
        logger.warning("没有匹配到pids")
        return [], [], [], []
    pid = pids[0]
    logger.info("获取到匹配度最高的pid:{}".format(pid))
    companyDetail(pid)
    global headers2
    # 获取网站备案、对外投资、控股企业、分支机构
    headers2 = headers
    headers2["Referer"]='https://aiqicha.baidu.com/company_detail_{}'.format(pid)
    headers2["Zx-Open-Url"]='https://aiqicha.baidu.com/company_detail_{}'.format(pid)
    url = r"https://aiqicha.baidu.com/compdata/navigationListAjax?pid={}".format(pid)
    # print(url)
    res = requests.get(url=url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
    text = res.text
    text = text.encode('utf-8').decode('unicode_escape')
    text_json = json.loads(text)
    basic, certRecord = [], []
    for _ in text_json["data"]:
        if _["id"] == "basic":
            # 基本信息
            basic = _["children"]
        if _["id"] == "certRecord":
            # 知识产权
            certRecord = _["children"]
    # print(basic)
    # print(certRecord)
    global invest_num, holds_num, branch_num, webRecord_num
    invest_num, holds_num, branch_num, webRecord_num = 0, 0, 0, 0
    # 网站备案
    for each in certRecord:
        if each["name"] == "网站备案":
            webRecord_num = each["total"]

    for each in basic:
        if each["name"] == "对外投资":
            invest_num = each["total"]
        if each["name"] == "控股企业":
            holds_num = each["total"]
        if each["name"] == "分支机构":
            branch_num = each["total"]
    logger.info("网站备案:{}\n对外投资:{}\n控股企业:{}\n分支机构:{}\n".format(webRecord_num, invest_num, holds_num, branch_num))
    if branch_num > 200:
        branch_num = 30
    # 页数
    icpinfo_page = webRecord_num // size + 1
    invest_page = invest_num // size + 1
    holds_page = holds_num // size + 1
    branch_page = branch_num // size + 1
    print()
    selfIcpinfo_infos = icpinfo(pid, icpinfo_page)

    invest(pid, invest_page)
    holds(pid, holds_page)
    branch(pid, branch_page)

    return selfIcpinfo_infos, invest_infos, holds_infos, branch_infos


def run_aiqicha(searchContent):
    selfIcpinfo_infos, invest_infos, holds_infos, branch_infos = start(searchContent)
    return selfIcpinfo_infos, invest_infos, holds_infos, branch_infos

