#!/usr/bin/python3
# coding: utf-8
import sys

from conf import config
from module import globals
from conf.log import logger
import time
from module import gadgets
import os
import re
import threading
import subprocess
import requests
import warnings
import json

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH=globals.get_value("RESULT_PATH")

if not os.path.exists(os.path.join(RESULT_PATH, "crawlergo")):
    os.makedirs(os.path.join(RESULT_PATH, "crawlergo"))
if not os.path.exists(os.path.join(RESULT_PATH, "xray")):
    os.makedirs(os.path.join(RESULT_PATH, "xray"))


def crawlergo_spider(target):
    # cmd = [f"{os.path.join(BASE_PATH,'tools','crawlergo','crawlergo.exe')}", "-c", f"{os.path.join(BASE_PATH,'tools','crawlergo','chrome-win','chrome.exe')}", "-t", "10", "-f", "smart",
    #        "--fuzz-path", "--custom-headers", json.dumps(get_random_headers()), "--push-to-proxy",
    #        "http://127.0.0.1:7777/", "--push-pool-max", "10", "--output-mode", "json", target]

    crawlergo_cmd = [f"{os.path.join(TOOLS_PATH, 'crawlergo', 'crawlergo')}", "-c",
                     f"{os.path.join(TOOLS_PATH, 'crawlergo', 'chrome', 'chrome')}", "-t", "10", "-f", "smart",
                     "--fuzz-path", "--push-pool-max", "10", "--output-mode", "json", target]
    subprocess_crawlergo = subprocess.Popen(crawlergo_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info("RUN COMMAND:"+" ".join(crawlergo_cmd))
    time.sleep(1)
    while subprocess_crawlergo.poll() is None:
        subprocess_crawlergo.stderr.flush()
        line2 = subprocess_crawlergo.stderr.readline().strip().decode()
        if line2:
            print(line2)
            if "Task finished" in line2:
                break
            line2=''
    output, error = subprocess_crawlergo.communicate()

    try:
        result = json.loads(output.decode().split("--[Mission Complete]--")[1])
    except:
        return
    req_urls = result["req_list"]
    sub_domain = result["sub_domain_list"]
    print(target)
    print("[crawl ok]")

    file_name = gadgets.string_to_file_name(target)
    try:
        for subd in sub_domain:
            print(subd)
        with open(os.path.join(RESULT_PATH, "crawlergo", f"{file_name}_sub_domains.json"), "w") as fp:
            json.dump(sub_domain, fp)
    except:
        pass
    try:
        for req_url in req_urls:
            print(req_url)
        with open(os.path.join(RESULT_PATH, "crawlergo", f"{file_name}_req_urls.json"), "w") as fp:
            json.dump(req_urls, fp)
    except Exception as e:
        print(e)
    print("[scanning]")


def xray_save_json(xray_html_result,xray_json_result):
    with open(xray_html_result, 'r',encoding="utf-8") as fp:
        html = fp.read()
    results = re.findall("<script class='web-vulns'>webVulns.push\((.*?)\)</script>", html)
    jsonlist = []
    for i in results:
        jsonlist.append(json.loads(i))
    with open(xray_json_result, 'w',encoding="utf-8") as fp:
        json.dump(jsonlist, fp)


def crawlergo_xray(targets,html_output_file,json_output_file):
    xray_cmd = [f"{os.path.join(TOOLS_PATH, 'xray', 'xray')}", 'webscan', '--listen',
                '127.0.0.1:7777',
                '--html-output',html_output_file]
    subprocess_xray = subprocess.Popen(xray_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    req_urls=[]
    sub_domains=[]
    for target in targets:
        crawlergo_cmd = [f"{os.path.join(TOOLS_PATH, 'crawlergo', 'crawlergo')}", "-c",
                         f"{os.path.join(TOOLS_PATH, 'crawlergo', 'chrome', 'chrome')}", "-t", "10", "-f", "smart",
                         "--fuzz-path", "--push-to-proxy",
                         "http://127.0.0.1:7777/", "--push-pool-max", "10", "--output-mode", "json", target]
        subprocess_crawlergo = subprocess.Popen(crawlergo_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("RUN COMMAND:" + " ".join(crawlergo_cmd))
        while subprocess_crawlergo.poll() is None:
            subprocess_crawlergo.stderr.flush()
            line2 = subprocess_crawlergo.stderr.readline().strip().decode()
            if line2:
                print(line2)
                if "Task finished" in line2:
                    break
                line2 = ''
        try:
            output, error = subprocess_crawlergo.communicate(timeout=15)
        except Exception as e:
            subprocess_crawlergo.kill()
            output, error  = subprocess_crawlergo.communicate()
            return None, None

        try:
            result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            req_urls += result["req_list"]
            sub_domains += result["sub_domain_list"]
        except Exception as e:
            print(logger.warning(target,e))
    time.sleep(1)
    logger.info("RUN COMMAND:" + " ".join(xray_cmd))
    time.sleep(0.1)
    while subprocess_xray.poll() is None:
        subprocess_xray.stdout.flush()
        line = subprocess_xray.stdout.readline().strip().decode()
        print(line)
        if "pending: 0" in line:
            break
    else:
        output, error = subprocess_xray.communicate()
    if not os.path.exists(html_output_file):
        subprocess_xray.kill()
        return None,None
    else:
        xray_save_json(html_output_file,json_output_file)
        subprocess_xray.kill()
        return req_urls,sub_domains




if __name__ == '__main__':
    # file = open("targets.txt")
    # for text in file.readlines():
    #     data1 = text.strip('\n')
    #     main(data1)
    url = "http://testphp.vulnweb.com/"
    crawlergo_spider(url)
    # crawlergo_xray(url)
    # print(json.dumps(get_random_headers()))
    # rsp = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output, error =rsp.communicate()
    # print(output.decode("UTF8"))
    # print(globals.get_value("BASE_PATH"))
    # print(os.path.join(BASE_PATH,'tools','crawlergo','chrome-win','chrome.exe'))
    # print(result)
