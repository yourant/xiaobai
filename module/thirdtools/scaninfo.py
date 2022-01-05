import sys

from conf import config
from module import globals
from conf.log import logger
import time
from module import gadgets
import subprocess
import os
import time

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH=globals.get_value("RESULT_PATH")
if not os.path.exists(os.path.join(RESULT_PATH, "scaninfo")):
    os.makedirs(os.path.join(RESULT_PATH, "scaninfo"))

def run_scaninfo(target,np=False):
    output_file=os.path.join(RESULT_PATH,"scaninfo","result")
    if np:
        scaninfo_cmd = [f"{os.path.join(TOOLS_PATH, 'scaninfo', 'scaninfo')}", '-np', '-p','0-65535',"-m","port",'-i',target,
                  "-o",output_file]
    else:
        scaninfo_cmd = [f"{os.path.join(TOOLS_PATH, 'scaninfo', 'scaninfo')}", '-p', '0-65535',"-m","port", '-i', target,
                        "-o", output_file]
    logger.info("RUN COMMAND:" + " ".join(scaninfo_cmd))
    subprocess_scaninfo = subprocess.Popen(scaninfo_cmd, stdout=sys.stdout,stderr=sys.stderr)
    subprocess_scaninfo.communicate()


    with open(output_file+".txt","r",encoding="utf-8") as fp:
        result=fp.readlines()
    return result
# def run_scaninfo_file(targets_file,output_file):
#     vulmap_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'vulmap', 'vulmap.py')}", '-f', targets_file,
#                   "--output-json",output_file]
#     subprocess_vulmap = subprocess.Popen(vulmap_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#     logger.info("RUN COMMAND:"+" ".join(vulmap_cmd))
#     while subprocess_vulmap.poll() is None:
#         subprocess_vulmap.stdout.flush()
#     #     subprocess_vulmap.stderr.flush()
#         try:
#             line1 = subprocess_vulmap.stdout.readline().strip().decode()
#         #     line2 = subprocess_vulmap.stderr.readline().strip().decode()
#             if line1:
#                 print(line1)
#                 line1=''
#         #     if line2:
#         #         print(line2)
#         #         line2=
#         except:
#             pass

if __name__ == '__main__':
    target="221.176.159.0/24"
    run_scaninfo(target)

