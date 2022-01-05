import sys
from module.mtime import now
from module import globals
from module import gadgets
import os
import json
import platform

# 初始化globals
globals.init()
# 获取并配置根目录
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
globals.set_value("BASE_PATH", BASE_PATH)
# 获取当前操作系统类型，并设置工具保存路径
SYSTEM = platform.system()
globals.set_value("SYSTEM", SYSTEM)
if (platform.system() == 'Windows'):
    TOOLS_PATH = os.path.join(BASE_PATH, "tools", "windows")
elif (platform.system() == 'Linux'):
    TOOLS_PATH = os.path.join(BASE_PATH, "tools", "linux")
else:
    sys.exit("")

globals.set_value("TOOLS_PATH", TOOLS_PATH)
# 设置结果保存位置
RESULT_PATH = os.path.join(BASE_PATH, "results")
globals.set_value("RESULT_PATH", RESULT_PATH)

# 设置log文件保存位置
LOG_PATH = os.path.join(BASE_PATH, "log", f"{gadgets.string_to_file_name(now.no_style_dated())}.log")
globals.set_value("LOG_PATH", LOG_PATH)

# 设置AWVS API KEY
AWVS_API_KEY=""
AWVS_URL=""
globals.set_value("AWVS_API_KEY",AWVS_API_KEY)
globals.set_value("AWVS_URL",AWVS_URL)


# 设置fofa key
FOFA_EMAIL = ""
globals.set_value("FOFA_EMAIL",FOFA_EMAIL)
FOFA_KEY = ""
globals.set_value("FOFA_KEY",FOFA_KEY)

# 设置zoomeye key
ZOOMEYE_API_KEY=""
globals.set_value("ZOOMEYE_API_KEY",ZOOMEYE_API_KEY)

# 设置360 Quake key
QUAKE_KEY=""
globals.set_value("QUAKE_KEY",QUAKE_KEY)


# 设置爱企查headers，包含cookie，https://beian.tianyancha.com
AIQICHA_HEADERS={
	}
globals.set_value("AIQICHA_HEADERS",AIQICHA_HEADERS)

# 设置天眼查headers，包含cookie，https://aiqicha.baidu.com
TIANYANCHA_HEADERS={
	}
globals.set_value("TIANYANCHA_HEADERS",TIANYANCHA_HEADERS)
