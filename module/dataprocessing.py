from conf import config
from module import globals
from module.colors import color
from conf.log import logger
import time
from module import gadgets
import subprocess
import os
import json
import IPy

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH = globals.get_value("RESULT_PATH")


def tainyancha2oneforall(input_file,output_file):
    logger.info("正在把天眼查爬到的数据处理为oneforall可爆破的格式。")
    with open(input_file,"r",encoding="utf-8") as fp:
        results=json.load(fp)
    domains=set()
    for result in results:
        domains.add(result["域名"])
    with open(output_file,'w',encoding="utf-8") as fp:
        fp.write("\n".join(domains))


def onforall2awvs(input_file,output_file):
    logger.info("正在把oneforall搜集到的数据处理为awvs可扫描的格式。")
    with open(input_file,"r",encoding="utf-8") as fp:
        json_resultss=json.load(fp)
    results=[]

    flags=[]
    for json_results in json_resultss:
        for json_result in json_results:
            if json_result["status"] is None and json_result["title"] is None:
                continue
            ip=json_result["ip"]
            title=json_result["title"].replace("\\n","").replace("\\xa0",'').replace("\\t","").replace("\\r","")
            url=json_result["url"]
            status=json_result["status"]
            flag=ip+title
            if flag in flags:
                continue
            if "404" in title or "系统未知异常" in title:
                continue
            result = {}
            flags.append(flag)
            result["title"]=title
            result["url"]=url
            results.append(result)
        with open(output_file, "w", encoding="utf-8") as fp:
            json.dump(results,fp,ensure_ascii=False,indent=4)

def onforallip2ips(input_file,output_file,cidr="28"):
    logger.info("正在把oneforall搜集到的ip进行聚合。")
    time.sleep(0.1)
    networks=set()
    with open(input_file,"r",encoding="utf-8") as fp:
        json_resultss=json.load(fp)
    for json_results in json_resultss:
        for json_result in json_results:
            ip=json_result["ip"]
            if "," in ip:
                continue
            if IPy.IP(ip).iptype() == 'PUBLIC':
                addr=json_result["addr"]
                network=gadgets.ipcidr_to_netmask(ip+"/"+cidr)[0]
                networks.add('ip="'+network+'"')

    with open(output_file,"w",encoding="utf-8") as fp:
        fp.write("\n".join(networks))

def fofa2protocol(input_file):
    results={}
    with open(input_file,'r',encoding="utf-8") as fp:
        json_resultss=json.load(fp)
    for json_results in json_resultss:
        for json_result in json_results:
            print(json_result)
            port=json_result[4]
            ip=json_result[3]
            protocol=json_result[2]
            title=json_result[1]
            url=json_result[0]
            if protocol=="" :
                if "https" in url:
                    protocol="https"
                    url=url.split("/")[-1].split(":")[0]
                elif "http" in url:
                    protocol = "http"
                    url = url.split("/")[-1].split(":")[0]
                else:
                    protocol = "http"
            if protocol in results.keys():
                results[protocol].append([ip,port,title,])
            else:
                results[protocol]=[]
                results[protocol].append([ip, port, title, ])
    with open(input_file, 'w', encoding="utf-8") as fp:
        json.dump(results,fp)

def fofa2awvs(input_file,output_file):
    results=[]
    with open(input_file,'r',encoding="utf-8") as fp:
        json_resultss=json.load(fp)
    for k,v in json_resultss.items():
        if k=="http":
            for i in v:
                url="http://"+i[0]+":"+i[1]
                title=i[2].strip()
                results.append({"title":title,"url":url})
        if k=="https":
            for i in v:
                url="https://"+i[0]+":"+i[1]
                title=i[2].strip()
                results.append({"title":title,"url":url})

    if os.path.exists(output_file):
        with open(output_file,"r",encoding="utf-8") as fp:
            old_result=json.load(fp)
            results+=old_result
        with open(output_file,"w",encoding="utf-8") as fp:
            json.dump(results,fp)
    else:
        with open(output_file,"w",encoding="utf-8") as fp:
            json.dump(results,fp)

def saveresult(input_file,output_file,modle):
    with open(input_file, "r", encoding="utf-8") as fp:
        tmp_result = json.load(fp)
    with open(output_file, 'r', encoding="utf-8") as fp:
        result = json.load(fp)
        result[modle] = tmp_result
    with open(output_file, 'w', encoding="utf-8") as fp:
        json.dump(result,fp)

def resultanalysis(inputfile):
    with open(inputfile,"r",encoding="utf-8") as fp:
        result=json.load(fp)
    for key in result.keys():
        if  key =="aaa":
            continue
        elif key=="fofa_ip":
            print(color.yel_info(),"fofa收集到的数据如下")
            for k, v in result["fofa_ip"].items():
                print("协议：",k)
                for i in v:
                    print(i)
        elif key=="domains":
            print(color.yel_info(),'共计发现的域名如下')
            for domain in result["domains"]:
                print(domain)
        elif key=="tianyancha":
            print(color.yel_info(),'tianyancha共计发现的企业信息如下')
            for tianyancha in result["tianyancha"]:
                print(tianyancha)
        elif key=="oneforall":
            print(color.yel_info(),'oneforall发现的子域名信息如下')
            for oneforall in result["oneforall"]:
                print(oneforall)
        elif key=="vulmap":
            print(color.yel_info(), "vulmap扫描到的结果如下")
            for vule in result["vulmap"]:
                # print(vule)
                print("漏洞位置:", vule["detail"]["url"])
                print("漏洞名称:",vule["detail"]["description"])
                print("发现模块:",vule["plugin"])
                print()
        elif key=="hydra":
            print(color.yel_info(), "hydra扫描到的结果如下")
            for vule in result["hydra"]:
                print(vule)
            print()
        elif key=="xray":
            print(color.yel_info(), "xray扫描到的结果如下")
            print(color.yel_info(), "扫描到的链接如下")
            for url in result["xray"]["urls"]:

                print(url["url"])
                # print(vule)
            print(color.yel_info(), "扫描到的子域名如下")
            for sub_domain in result["xray"]["sub_domains"]:
                print(sub_domain)
            print(color.yel_info(), "发现的问题如下")
            for vule in result["xray"]["result"]:
                print("漏洞位置:", vule["detail"]["addr"])
                print("payload:",vule["detail"]["payload"])
                print("发现模块:",vule["plugin"])
                print()
        else:
            print(key)
            print(result[key])
