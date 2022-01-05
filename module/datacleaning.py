from conf import config
from module import globals
from conf.log import logger
import shutil
import time
from module import gadgets
import subprocess
import os
import json

BASE_PATH = globals.get_value("BASE_PATH")
TOOLS_PATH = globals.get_value("TOOLS_PATH")
RESULT_PATH = globals.get_value("RESULT_PATH")


def scan_url_clean(self, input_file):
    with open(input_file, "r", encoding="utf-8") as fp:
        results = json.load(fp)
    urls_title = {}
    urls = []
    for result in results:
        if result["url"] in urls and result["title"] != "":
            urls_title[result["url"]] = result["title"]
        else:
            urls_title[result["url"]] = result["title"]
            urls.append(result["url"])
    json_result = []
    for k, v in urls_title.items():
        json_result.append({"url": k, "title": v})
    with open(input_file, "w", encoding="utf-8") as fp:
        json.dump(json_result, fp)


def tianyancha_data_filter(keyword, filter: dict, file):
    logger.info(f"正在对{keyword}关键词爬取的数据根据{filter}进行过滤清洗")
    results = []
    with open(file, 'r') as fp:
        tmp_results = json.load(fp)
    filter = json.loads(filter)
    for filter_key, filter_values in filter.items():
        for filter_value in filter_values.split(","):
            for result in tmp_results:
                if filter_value in result[filter_key]:
                    results.append(result)
    with open(file, 'w', encoding="utf-8") as fp:
        json.dump(results, fp, indent=4, ensure_ascii=False)


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def data_file_clean():
    del_file(os.path.join(BASE_PATH, "input"))
    files_dir = ['crawlergo', 'dismap', 'fofa', 'oneforall', 'tianyancha', 'vulmap', 'xray', 'hydra', 'scaninfo']
    for file_dir in files_dir:
        del_file(os.path.join(RESULT_PATH, file_dir))
    del_file(os.path.join(TOOLS_PATH, "oneforall", "results"))


if __name__ == '__main__':
    data_file_clean()
