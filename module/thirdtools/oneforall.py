import json

from conf import config
from module import globals
from conf.log import logger
import time
from module import gadgets
import subprocess
import os

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH=globals.get_value("RESULT_PATH")
if not os.path.exists(os.path.join(RESULT_PATH, "oneforall")):
    os.makedirs(os.path.join(RESULT_PATH, "oneforall"))
def run_oneforall(target):
    oneforall_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'oneforall', 'oneforall.py')}", '--target', target,
                     '--fmt', 'json', '--path',os.path.join(RESULT_PATH, "oneforall"),'run']
    subprocess_oneforall = subprocess.Popen(oneforall_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    logger.info("RUN COMMAND:"+" ".join(oneforall_cmd))
    while subprocess_oneforall.poll() is None:
        # subprocess_oneforall.stdout.flush()
        subprocess_oneforall.stderr.flush()
        # line1 = subprocess_oneforall.stdout.readline().strip().decode()
        line2 = subprocess_oneforall.stderr.readline().strip().decode()
        # if line1:
        #     print(line1)
        #     line1=''
        if line2:
            print(line2)
            line2=''
def run_oneforall_file(targetfile,outputfile):
    oneforall_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'oneforall', 'oneforall.py')}", '--targets', targetfile,
                     '--fmt', 'json', '--path',os.path.join(RESULT_PATH, "oneforall"),'run']
    subprocess_oneforall = subprocess.Popen(oneforall_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    logger.info("RUN COMMAND:"+" ".join(oneforall_cmd))
    while subprocess_oneforall.poll() is None:
        # subprocess_oneforall.stdout.flush()
        subprocess_oneforall.stderr.flush()
        # line1 = subprocess_oneforall.stdout.readline().strip().decode()
        try:
            line2 = subprocess_oneforall.stderr.readline().strip().decode()
        except:
            pass
        if line2:
            print(line2)
            line2=''
    results=[]
    with open( targetfile,"r",encoding="utf-8") as fp:
        txt_results=fp.readlines()
    for txt_result in txt_results:
        try:
            with open(os.path.join(RESULT_PATH, "oneforall",txt_result.strip()+".json"), "r", encoding="utf-8") as fp:
                json_result=json.load(fp)
                results.append(json_result)
        except:
            logger.warning(txt_result.strip()+".json"+"文件不存在")
    with open(outputfile, "w", encoding="utf-8") as fp:
        json.dump(results,fp,indent=4, ensure_ascii=False)
if __name__ == '__main__':
    run_oneforall("nyist.edu.cn")
# from bs4 import BeautifulSoup
#
# soup=BeautifulSoup("aaa","lxml")
# soup.