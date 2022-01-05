import sys

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
RESULT_PATH = os.path.join(globals.get_value("RESULT_PATH"),"dismap")

if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)

def run_dismap_scan_ip(targets,np=False):
    if np:
        dismap_cmd = [os.path.join(TOOLS_PATH,"dismap","dismap"),'-np','-output',os.path.join(RESULT_PATH,f"{gadgets.string_to_file_name(targets)}.txt"), '-ip', targets]
    else:
        dismap_cmd = [os.path.join(TOOLS_PATH,"dismap","dismap"),'-output',os.path.join(RESULT_PATH,f"{gadgets.string_to_file_name(targets)}.txt"), '-ip', targets]
    logger.info("RUN COMMAND:" + " ".join(dismap_cmd))
    time.sleep(0.1)
    subprocess_dismap = subprocess.Popen(dismap_cmd, stdout=sys.stdout,stderr=sys.stderr)
    subprocess_dismap.communicate()
    results_json=[]
    with open(os.path.join(RESULT_PATH,f"{gadgets.string_to_file_name(targets)}.txt"),"r",encoding="utf-8") as fp:
        results=fp.readlines()
    for i in results:
        if i.startswith("["):
            result_json = {}
            tmp=i.replace("[",'').replace("]",'').replace("{ ","_").replace(" }","_").strip().split("_")
            status_code=tmp[0].split()[1]
            middleware=tmp[0].split()[2:]
            title=tmp[-1].strip()
            url=tmp[1]
            result_json["url"]=url
            result_json["status_code"]=status_code
            result_json["middleware"]=middleware
            result_json["title"]=title
            results_json.append(result_json)

    return results_json




if __name__ == '__main__':
    run_dismap_scan_ip("47.105.92.0/24")
    # targets="47.105.92.0/24"

