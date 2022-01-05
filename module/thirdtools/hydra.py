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
RESULT_PATH = os.path.join(globals.get_value("RESULT_PATH"),"hydra")
if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)

def run_hydra(services):
    results=[]
    for service in services.keys():
        with open(os.path.join(BASE_PATH,"input",f"{service}.txt"),"w",encoding="utf-8") as fp:
            fp.write("\n".join(services[service]))

    for service in services.keys():
        hydra_cmd = ["hydra",'-vV','-I','-t','30','-L',os.path.join(BASE_PATH,'dict','hydra',f"{service}-user.txt"), '-P', os.path.join(BASE_PATH,'dict','hydra',f"{service}-passwd.txt"),"-M",os.path.join(BASE_PATH,'input',f"{service}.txt"),'-o',os.path.join(RESULT_PATH,"hydra.txt"),service]
        logger.info("RUN COMMAND:" + " ".join(hydra_cmd))
        time.sleep(0.1)
        subprocess_hydra = subprocess.Popen(hydra_cmd, stdout=sys.stdout,stderr=sys.stderr)
        subprocess_hydra.communicate()

        if os.path.exists(os.path.join(RESULT_PATH,"hydra.txt")):
            with open(os.path.join(RESULT_PATH,"hydra.txt"),"r",encoding="utf-8") as fp:
                lines=fp.readlines()
            for line in lines:
                if not line.startswith("#"):
                    results.append(line.strip())
    return results

