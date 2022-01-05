import sys

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
if not os.path.exists(os.path.join(RESULT_PATH, "vulmap")):
    os.makedirs(os.path.join(RESULT_PATH, "vulmap"))

def run_vulmap(target):
    vulmap_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'vulmap', 'vulmap.py')}", '-u', target,
                  "--output-json",os.path.join(RESULT_PATH,"vulmap",f"{gadgets.string_to_file_name(target)}.json")]
    logger.info("RUN COMMAND:" + " ".join(vulmap_cmd))

    subprocess_vulmap = subprocess.Popen(vulmap_cmd, stdout=sys.stdout,stderr=sys.stderr)

    subprocess_vulmap.communicate()

def run_vulmap_file(targets_file,output_file):
    vulmap_cmd = ["python3", f"{os.path.join(TOOLS_PATH, 'vulmap', 'vulmap.py')}", '-f', targets_file,
                  "--output-json",output_file]
    logger.info("RUN COMMAND:" + " ".join(vulmap_cmd))
    time.sleep(0.1)
    subprocess_vulmap = subprocess.Popen(vulmap_cmd, stdout=sys.stdout,stderr=sys.stderr)
    subprocess_vulmap.communicate()


if __name__ == '__main__':
    target="http://117.158.106.69:8081"
    run_vulmap(target)



