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
RESULT_PATH=globals.get_value("RESULT_PATH")


if not os.path.exists(os.path.join(RESULT_PATH, "webcrack")):
    os.makedirs(os.path.join(RESULT_PATH, "webcrack"))

def run_webcrack(target):
    webcrack_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'webcrack', 'webcrack.py')}", target]
    subprocess_vulmap = subprocess.Popen(webcrack_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    logger.info("RUN COMMAND:"+" ".join(webcrack_cmd))
    while subprocess_vulmap.poll() is None:
        subprocess_vulmap.stdout.flush()
    #     subprocess_vulmap.stderr.flush()
        line1 = subprocess_vulmap.stdout.readline().strip().decode()
    #     line2 = subprocess_vulmap.stderr.readline().strip().decode()
        if line1:
            print(line1)
            line1=''
    #     if line2:
    #         print(line2)
    #         line2=
    success_targes = ''
    if not os.path.exists(os.path.join(TOOLS_PATH,"webcrack","logs","success.txt")):
        try:
            with open(os.path.join(TOOLS_PATH,"webcrack","logs","success.txt"),"r") as fp:
                success_targes=fp.readlines()
            result={}
            with open(os.path.join(RESULT_PATH, "webcrack", "result.json"), "r", encoding="utf-8") as fp:
                results=json.load(fp)
        except Exception as e:
            logger.warning(e)
    elif os.path.exists(os.path.join(TOOLS_PATH,"webcrack","logs","success.txt")):
        try:
            with open(os.path.join(TOOLS_PATH,"webcrack","logs","success.txt"),"r") as fp:
                success_targes=fp.readlines()
            result={}
            results =[]
        except Exception as e:
            logger.warning(e)
    if success_targes:
        for success_targe in success_targes:
            tmp=success_targe.strip().split(" ")
            result["url"]=tmp[-3]
            result["usernamee"]=tmp[-1].split("/")[0]
            result["password"]=tmp[-1].split("/")[1]
            results.append(result)
        with open(os.path.join(RESULT_PATH,"webcrack","result.json"),"w",encoding="utf-8") as fp:
            json.dump(results,fp,indent=4, ensure_ascii=False)
        os.remove(os.path.join(TOOLS_PATH,"webcrack","logs","success.txt"))
if __name__ == '__main__':
    run_webcrack("http://139.224.53.226/login")