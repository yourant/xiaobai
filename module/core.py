import sys
from IPy import IP
from tld import get_tld
from conf import config
from conf.argparse import arg
from module import globals
from module.api.tianyancha_api import tianyancha
from module.thirdtools import vulmap
from module.thirdtools import nmap
from module.thirdtools import oneforall
from module import datacleaning
from module import dataprocessing
from module.api import aiqicha_api
from module.thirdtools import hydra
from module.thirdtools import dismap
from module.api import zoomeye_api
from module.api.awvs_api import awvsapi
from module.thirdtools import oneforall
from conf.log import logger
from module.thirdtools import scaninfo
import time
from module.api.fofa_api import fofa
from module import gadgets
import subprocess
import os
import json
import shutil
from module.thirdtools import crawlergo_xray

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH = globals.get_value("RESULT_PATH")
RESULT={}

RESULT["ips"]=set()

def run_tianyancha(keywords,filter_keyword=None):
    RESULT["domains"] = set()
    if len(keywords)==1:
        keyword=keywords[0]
        result_path = os.path.join(RESULT_PATH, "tianyancha", "tmp.json")
        tianyancha.search_keyword(keyword,result_path)
        if filter_keyword:
            datacleaning.tianyancha_data_filter(keyword,filter_keyword,result_path)
        with open(result_path,"r",encoding="utf-8") as fp:
            RESULT["tianyancha"]=json.load(fp)
    else:
        result_path = os.path.join(RESULT_PATH, "tianyancha", "tmp.json")
        for keyword in keywords:
            tmp_result = []
            tianyancha.search_keyword(keyword, result_path)
            if filter_keyword:
                datacleaning.tianyancha_data_filter(keyword, filter_keyword, result_path)
            with open(result_path, "r", encoding="utf-8") as fp:
                tmp_result += json.load(fp)
        RESULT["tianyancha"] = tmp_result
    for result in RESULT["tianyancha"]:
        RESULT["domains"].add(result["域名"])
    RESULT["domains"] = list(RESULT["domains"])

def run_oneforall(domains,cidr):
    input_path=os.path.join(BASE_PATH,"input","oneforall.txt")
    output_file=os.path.join(RESULT_PATH,"oneforall","oneforall.json")
    with open(input_path,"w",encoding="utf-8") as fp:
        fp.write("\n".join(domains))
    oneforall.run_oneforall_file(input_path,output_file)
    with open(output_file, "r", encoding="utf-8") as fp:
        tmpss=json.load(fp)
    ip_title = []
    for tmps in tmpss:
        for tmp in tmps:
            title=tmp["title"]
            ip=tmp["ip"]

            if title is None :
                title="None"
            if ip+title in ip_title:
                continue
            if "oneforall" in RESULT.keys():
                RESULT["oneforall"].append({"url":tmp["url"],"title":tmp["title"],"ip":tmp["ip"]})
                ip_title.append(ip+title)
                RESULT["ips"].add(ip)
            else:
                RESULT["oneforall"]=[]
                RESULT["oneforall"].append({"url":tmp["url"],"title":tmp["title"],"ip":tmp["ip"]})
                ip_title.append(ip + title)
                RESULT["ips"].add(ip)
    ips=RESULT["ips"]
    networks = {}
    for ip in ips:
        if "," in ip:
            continue
        if IP(ip).iptype() != 'PUBLIC':
            continue
        network, netmask, ip = gadgets.ipcidr_to_netmask(ip, cidr)
        if network in networks.keys():
            networks[network] += 1
        else:
            networks[network] = 1
    RESULT["ips"] = networks

def run_fofa_ip(networks):
    results=[]
    tmp_results={}
    for network in networks:
        result=fofa.get_search(f'ip="{network}"',size=10000)
        if result:
            results+=result
    for result in results:
        protocol=result[2]
        ip=result[3]
        port=result[4]
        title=result[1]
        if protocol=="":
            protocol="http"
        if protocol in tmp_results.keys():
            tmp_results[protocol].append([ip,port,title])
        else:
            tmp_results[protocol]=[]
            tmp_results[protocol].append([ip, port, title])
    RESULT["fofa_ip"]=tmp_results

def run_awvs():
    for url, title in RESULT["urls"]:
        awvsapi.create_target_and_scan(url, title)

def run_hydra():
    services=RESULT["services"]
    results=hydra.run_hydra(services)
    RESULT["hydra"]=results

def run_vulmap():
    input_file=os.path.join(BASE_PATH,"input","urls.txt")
    output_file=os.path.join(RESULT_PATH,"vulmap","vulmap.json")
    with open(input_file,"w",encoding="utf-8") as fp:
        fp.write("\n".join([_[0] for _ in RESULT["urls"]]))
    vulmap.run_vulmap_file(input_file,output_file)
    if os.path.exists(output_file):
        with open(output_file,"r",encoding="utf-8") as fp:
            result=json.load(fp)
        RESULT["vulmap"]=result

def run_xray():
    urls=[_[0] for _ in RESULT["urls"]]
    html_output_file=os.path.join(RESULT_PATH,"xray","xray.html")
    json_output_file=os.path.join(RESULT_PATH,"xray","xray.json")
    req_urls,sub_domains=crawlergo_xray.crawlergo_xray(urls,html_output_file,json_output_file)
    if os.path.exists(json_output_file):
        with open(json_output_file,'r',encoding="utf-8") as fp:
            result=json.load(fp)
        RESULT["xray"]={"urls":req_urls,"sub_domains":sub_domains,"result":result}

def run_quake(networks):
    results=[]
    tmp_results={}
    for network in networks:
        result=fofa.get_search(f'ip:{network}"',size=1000)
        if result:
            results+=result
    for result in results:
        ip=result[2]
        port=result[4]
        title=result[1]
        protocol=result[6]
        if protocol =="http/ssl":
            protocol=="https"
            # print(protocol,ip,port,title)
        if protocol in tmp_results.keys():
            tmp_results[protocol].append([ip,port,title])
        else:
            tmp_results[protocol]=[]
            tmp_results[protocol].append([ip, port, title])
    RESULT["quake_ip"]=tmp_results


def run_aiqicha(companys,filter_keyword=None):
    RESULT["domains"]=set()
    results=[]
    for compay in companys:
        results.append(aiqicha_api.run_aiqicha(compay))
    RESULT["aiqicha"]=results
    if not results:
        logger.error("未查询到信息。")
    for result in results:
        if result[0]:
            for i in result[0]:
                if "domain" in i.keys():
                    for domain in i["domain"]:
                        RESULT["domains"].add(domain)
        if filter_keyword:
            if "invest_info" in filter_keyword and result[1]:
                for i in result[1]:
                    if i['icp_info']:
                        for domains in i['icp_info']:
                            for domain in domains["domain"]:
                                RESULT["domains"].add(domain)
            if "holds_info" in filter_keyword and result[2]:
                for i in result[2]:
                    if i['icp_info']:
                        for domains in i['icp_info']:
                            for domain in domains["domain"]:
                                RESULT["domains"].add(domain)
            if "branch_info" in filter_keyword and result[3]:
                for i in result[3]:
                    if i['icp_info']:
                        for domains in i['icp_info']:
                            for domain in domains["domain"]:
                                RESULT["domains"].add(domain)
        else:
            for num in range(1, 4):
                if result[num]:
                    for i in result[1]:
                        if i['icp_info']:
                            for domains in i['icp_info']:
                                for domain in domains["domain"]:
                                    RESULT["domains"].add(domain)
    RESULT["domains"]=list(RESULT["domains"])

def run_dismap(networks,np):
    dismap_result=[]
    for network in networks:
        dismap_result+=dismap.run_dismap_scan_ip(network,np)
    if dismap_result:
        RESULT["dismap"]=dismap_result

def run_zoomeye_ip(networks):
    results = []
    tmp_results = {}
    for network in networks:
        results += zoomeye_api.zoomeyeapi.zoom_search(f'cidr:{network}')
    for result in results:
        protocol = result[2]
        ip = result[0]
        port = result[1]
        title = ""
        if protocol == "":
            protocol = "http"
        if protocol in tmp_results.keys():
            tmp_results[protocol].append([ip, port, title])
        else:
            tmp_results[protocol] = []
            tmp_results[protocol].append([ip, port, title])
    RESULT["zoomeye_ip"] = tmp_results

def run_scaninfo(networks,np):
    scaninfo_result=[]
    for network in networks:
        scaninfo_result+=scaninfo.run_scaninfo(network,np)
    if scaninfo_result:
        RESULT["scaninfo"]=scaninfo_result

def run_nmap(networks,ports,np):
    nmap_result=[]
    for network in networks:
        nmap_result+=nmap.run_nmap(network,ports,np)
    if nmap_result:
        RESULT["nmap"]=nmap_result

def get_urls():
    urls=[]
    tmp_urls=[]
    keys=RESULT.keys()
    if "oneforall" in keys:
        for result in RESULT["oneforall"]:
            url=result["url"]
            title=result["title"]
            if title ==None:
                title=""
            if url in tmp_urls:
                continue
            tmp_urls.append(url)
            urls.append([url,title.strip()])
    if "nmap" in keys:
        for result in RESULT["nmap"]:
            ip = result["ip"]
            port = result["port"]
            service = result["service"]
            if service =="http" or service =="https":
                urls.append([f"{service}://{ip}:{port}",""])
    if "scaninfo" in keys:
        for result in RESULT["scaninfo"]:
            result=json.loads(result)
            url=result["url"]
            title=""
            if url in tmp_urls:
                continue
            tmp_urls.append(url)
            urls.append([url,title])
    if "dismap" in keys:
        for result in RESULT["dismap"]:
            url=result["url"]
            title=result["title"]
            if title ==None:
                title=""
            if url in tmp_urls:
                continue
            tmp_urls.append(url)
            urls.append([url,title.strip()])
    modules = ["fofa_ip", "zoomeye_ip","quake_ip"]
    for module in modules:
        if module in keys:
            if "http" in RESULT[module].keys():
                for result in RESULT[module]["http"]:
                    url=f"http://{result[0]}:{result[1]}"
                    title=result[-1]
                    if title ==None:
                        title=""
                    if url in tmp_urls:
                        continue
                    tmp_urls.append(url)
                    urls.append([url, title.strip()])
            if "https" in RESULT[module].keys():
                for result in RESULT[module]["https"]:
                    url=f"https://{result[0]}:{result[1]}"
                    title=result[-1].strip()
                    if title ==None:
                        title=""
                    if url in tmp_urls:
                        continue
                    tmp_urls.append(url)
                    urls.append([url, title.strip()])
    if "urls" in RESULT.keys():
        RESULT["urls"]+=urls
    else:
        RESULT["urls"] = urls
    black_keyword=["写真","小说","游戏","棋牌","赌球", "小说","家具维修","餐饮装修","运势","餐饮装修","施工电梯","游乐设备","社交平台",""]
    tmp_urls_results=[]
    black_domains=[]
    black_urls=[]
    urls_results = RESULT["urls"]
    for urls_result in urls_results:
        url=urls_result[0]
        title=urls_result[1]
        for keyword in black_keyword:
            if keyword in title:
                try:
                    domain=get_tld(url,as_object=False).fld
                    black_domains.append(domain)
                except:
                    black_urls.append(url)
    for urls_result in urls_results:
        url = urls_result[0]
        title = urls_result[1]
        if black_domains:
            try:
                domain = get_tld(url, as_object=False).fld
                if domain in black_domains:
                    continue
                else:

                    tmp_urls_results.append([url,title])
            except:
                if url not in black_urls:
                    tmp_urls_results.append([url, title])
        else:
            tmp_urls_results.append([url, title])
    RESULT["urls"] = tmp_urls_results

def get_services():
    ssh_services=set()
    ftp_services=set()
    mssql_services=set()
    mysql_services=set()
    rdp_services=set()
    keys=RESULT.keys()
    module0=["scaninfo","nmap"]
    for module in module0:
        if module in keys:
            for result in RESULT[module]:
                if isinstance(result,str):
                    result=json.loads(result)
                ip=result["ip"]
                port=result["port"]
                service=result["service"]
                if service=="ssh" and port=="22":
                    ssh_services.add(ip)
                elif service=="ftp" and port=="21":
                    ftp_services.add(ip)
                elif service=="mssql" and port=="1433":
                    mssql_services.add(ip)
                elif service=="mysql" and port=="3306":
                    mysql_services.add(ip)
                elif service=="rdp" and port=="3389":
                    rdp_services.add(ip)
                elif service=="ms-wbt-server" and port=="3389":
                    rdp_services.add(ip)
    modules1 = ["fofa_ip", "zoomeye_ip","quake_ip"]
    for module in modules1:
        if module in keys:
            if "ssh" in RESULT[module].keys():
                for result in RESULT[module]["ssh"]:
                    if result[1]=="22":
                        ssh_services.add(result[0])
            if "ftp" in RESULT[module].keys():
                for result in RESULT[module]["ftp"]:
                    if result[1]=="21":
                        ftp_services.add(result[0])
            if "mssql" in RESULT[module].keys():
                for result in RESULT[module]["mssql"]:
                    if result[1]=="1433":
                        mssql_services.add(result[0])
            if "mysql" in RESULT[module].keys():
                for result in RESULT[module]["mysql"]:
                    if result[1]=="3306":
                        mysql_services.add(result[0])
            if "rdp" in RESULT[module].keys():
                for result in RESULT[module]["rdp"]:
                    if result[1]=="3389":
                        rdp_services.add(result[0])
    if "services" not in RESULT.keys():
        RESULT["services"]={}
    if ssh_services:
        RESULT["services"]["ssh"]=list(ssh_services)
    if ftp_services:
        RESULT["services"]["ftp"]=list(ftp_services)
    if mysql_services:
        RESULT["services"]["mysql"]=list(mysql_services)
    if mssql_services:
        RESULT["services"]["mssql"]=list(mssql_services)
    if rdp_services:
        RESULT["services"]["rdp"]=list(rdp_services)
def core(args):
    datacleaning.data_file_clean()
    keyword =args.keyword
    keywordfile=args.keywordfile
    filter_keyword = args.filter
    vulscan = args.vulscan
    ipsearch=args.ipsearch
    cidr = args.cidr
    ports=args.ports
    if not cidr:
        cidr=32
    ip=args.ip
    ipfile=args.ipfile
    url=args.url
    urlfile=args.urlfile
    domainfile=args.domainfile
    domain=args.domainfile
    title=args.title
    company=args.company
    companyfile = args.companyfile
    np=args.noping
    if keyword:
        RESULT["keywords"]=[keyword]
    elif keywordfile:
        if not os.path.exists(keywordfile):
            logger.error(keywordfile, "not exist。")
            sys.exit()
        keywords=[]
        with open(keywordfile, 'r', encoding="utf-8") as fp:
            for _ in fp.readlines():
                _=_.strip()
                if _ =="":
                    continue
                keywords.append(_)
        RESULT["keywords"] = keywords
    if company:
        RESULT["companys"]=[company]
    elif companyfile:
        if not os.path.exists(companyfile):
            logger.error(companyfile, "not exist。")
            sys.exit()
        with open(companyfile, 'r', encoding="utf-8") as fp:
            companys = [_.strip() for _ in fp.readlines()]
        RESULT["companys"] = companys
    if ip:
        if not gadgets.isIP(ip):
            logger.error(ip,"not a ip address")
            sys.exit()
        networks={}
        network, netmask, ip = gadgets.ipcidr_to_netmask(ip, cidr)
        networks[network] = 1
        RESULT["ips"] = networks
    elif ipfile:
        if not os.path.exists(ipfile):
            logger.error(ipfile,"not exist。")
            sys.exit()
        with open(ipfile,'r',encoding="utf-8") as fp:
            ips=[_.strip() for _ in fp.readlines()]
        networks = {}
        for ip in ips:
            if "," in ip or not gadgets.isIP(ip):
                logger.error(ip,"not a ip address")
                continue
            if IP(ip).iptype() != 'PUBLIC':
                logger.error(ip,"not a PUBLIC ip")
                continue
            network, netmask, ip = gadgets.ipcidr_to_netmask(ip, cidr)
            if network in networks.keys():
                networks[network] += 1
            else:
                networks[network] = 1
        RESULT["ips"] = networks
    if domain:
        RESULT["domains"]=[domain]
    elif domainfile:
        if not os.path.exists(ipfile):
            logger.error(ipfile,"not exist。")
            sys.exit()
        with open(ipfile,'r',encoding="utf-8") as fp:
            domains=[_.strip() for _ in fp.readlines()]
        RESULT["domains"]=domains
    if url:
        if not title:
            title=""
        RESULT["urls"]=[[url,title]]
    if urlfile:
        if not os.path.exists(ipfile):
            logger.error(urlfile,"not exist。")
            sys.exit()
        with open(urlfile,"r",encoding="utf-8"):
            urls=[_.split(",") for _ in fp.readlines()]
        RESULT["urls"] = [[url, title]]
    # try:
    if keyword or keywordfile:
        keywords=RESULT["keywords"]
        run_tianyancha(keywords,filter_keyword)
        domains = RESULT["domains"]
        run_oneforall(domains,cidr)
    if domain or domainfile:
        domains = RESULT["domains"]
        run_oneforall(domains, cidr)
    if company or companyfile:
        companys=RESULT["companys"]
        run_aiqicha(companys,filter_keyword)
        domains = RESULT["domains"]
        run_oneforall(domains, cidr)
    if ipsearch :
        ips=RESULT["ips"]
        if "fofa" in ipsearch:
            run_fofa_ip(ips.keys())
        if "dismap" in ipsearch:
            run_dismap(ips.keys(),np)
        if "zoomeye" in ipsearch:
            run_zoomeye_ip(ips.keys())
        if "scaninfo" in ipsearch:
            run_scaninfo(ips.keys(),np)
        if "nmap" in ipsearch:
            run_nmap(ips.keys(),ports,np)
    get_urls()
    get_services()
    if vulscan:
        if "awvs" in vulscan:
            run_awvs()
        if "xray" in vulscan:
            run_xray()
        if "vulmap" in vulscan:
            run_vulmap()
        if "hydra" in vulscan:
            run_hydra()
    with open(os.path.join(RESULT_PATH,"result.json"),'w',encoding="utf-8") as fp:
        if not RESULT["ips"]:
            del RESULT["ips"]
        json.dump(RESULT,fp,indent=4,ensure_ascii=False)
    dataprocessing.resultanalysis(os.path.join(RESULT_PATH,"result.json"))
    # datacleaning.data_file_clean()



if __name__ == '__main__':
    core()