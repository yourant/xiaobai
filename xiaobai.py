from conf import config
from conf.argparse import arg
from module import globals
from conf.log import logger
import time
from module import core
from module import gadgets
import subprocess
import os
import json
def banner():
    banner = """
           __                      __                  __ 
          /  |                    /  |                /  |
 __    __ $$/   ______    ______  $$ |____    ______  $$/ 
/  \  /  |/  | /      \  /      \ $$      \  /      \ /  |
$$  \/$$/ $$ | $$$$$$  |/$$$$$$  |$$$$$$$  | $$$$$$  |$$ |
 $$  $$<  $$ | /    $$ |$$ |  $$ |$$ |  $$ | /    $$ |$$ |
 /$$$$  \ $$ |/$$$$$$$ |$$ \__$$ |$$ |__$$ |/$$$$$$$ |$$ |
/$$/ $$  |$$ |$$    $$ |$$    $$/ $$    $$/ $$    $$ |$$ |
$$/   $$/ $$/  $$$$$$$/  $$$$$$/  $$$$$$$/   $$$$$$$/ $$/ 

"""

    print(banner)

def main():
    banner()
    args=arg()
    core.core(args)

if __name__ == '__main__':
    main()