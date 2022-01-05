import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from module import globals
from conf.log import logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AwvsApi:
    def __init__(self, url, api_key):
        self.url = url
        self.headers = {
            'X-Auth': f'{api_key}',
            'Content-type': 'application/json'
        }

    def get_awvs_version_info(self):
        '''
        获取awvs用户信息，主要包含以下字段：targets（目标详细信息）、pagination（分页信息）。
        :return:dict数据
        '''
        result = {}
        api_url = f'{self.url}/api/v1/info'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        result["版本号"] = f'{r["major_version"]}.{r["minor_version"]}.{r["build_number"]}'
        result["许可证密钥"] = r["license"]["license_key"]
        result["产品状态"] = r["license"]["maintenance_expires"]
        return result

    def get_awvs_user_info(self):
        '''
        获取awvs用户信息。
        :return:dict数据
        '''
        result = {}
        api_url = f'{self.url}/api/v1/me'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        result["当前账户名"] = r["first_name"]
        result["Email地址"] = r["email"]
        result["当前账户是否启用"] = r["enabled"]
        result["是否最高权限"] = r["su"]
        result["是否子账户"] = r["child_account"]
        result["当前用户id"] = r["user_id"]
        result["是否启用toptp"] = r["totp_enabled"]
        return result

    def get_awvs_dashboard_info(self):
        '''
        获取awvs首页面板展示信息。
        :return:dict数据
        '''
        result = {}
        api_url = f'{self.url}/api/v1/me/stats'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        result["最脆弱的目标"] = r["most_vulnerable_targets"]
        result["总进行扫描个数"] = r["scans_conducted_count"]
        result["正在扫描的个数"] = r["scans_running_count"]
        result["等待扫描的个数"] = r["scans_waiting_count"]
        result["总进行扫描个数"] = r["targets_count"]
        result["排名靠前漏洞分布"] = r["top_vulnerabilities"]
        result["通过危险程度进行漏洞等级个数分布"] = r["vuln_count_by_criticality"]
        result["漏洞数据"] = r["vuln_count"]
        result["通过危险程度进行漏洞等级个数分布"] = r["vuln_count_by_criticality"]
        result["排名靠前漏洞分布"] = r["top_vulnerabilities"]
        result["共发现漏洞总数"] = r["vulnerabilities_open_count"]
        return result

    def get_all_targets_info(self):
        '''
        获取AWVS中存在的所有target信息，返回list数据，其中每个目标的信息组合成一个字典，包含address、address、target_id信息。
        :return: list
        '''
        targets = []
        api_url = f'{self.url}/api/v1/targets'
        params = (("c", 0), ("l", 1))
        r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
        count = r["pagination"]["count"]
        num = int(int(count) / 100) + 1
        for i in range(num):
            params = (("c", i * 100), ("l", 100))
            api_url = f'{self.url}/api/v1/targets'
            r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
            tmp_targets = r["targets"]
            for target in tmp_targets:
                tmp = {"address": target["address"],
                       "description": target["description"],
                       "target_id": target["target_id"]}
                targets.append(tmp)
        return targets

    def get_targets_info_by_key_word(self, key_word):
        '''
        根据关键字获取AWVS中存在的target信息，返回list数据，其中每个目标的信息组合成一个字典，包含address、address、target_id信息。
        :param key_word: 要搜索的关键字，如域名、描述等信息
        :return: list
        '''
        targets = []
        params = (("q", f"text_search:*{key_word}"),)
        api_url = f'{self.url}/api/v1/targets'
        r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
        tmp_targets = r["targets"]
        print(tmp_targets)
        for target in tmp_targets:
            targets.append({"address": target["address"],
                            "description": target["description"],
                            "target_id": target["target_id"]})
        return targets

    def create_target(self, address, description, int_criticality=10):
        '''
        添加target信息,返回str，及target_id。
        :param address:目标地址
        :param description: 目标描述
        :param int_criticality: 重要等级，默认为10
        :return: str
        '''
        api_url = f'{self.url}/api/v1/targets'
        values = {
            'address': address,
            'description': description,
            'criticality': int_criticality,
        }
        data = json.dumps(values)
        target_id = requests.post(api_url, data, headers=self.headers, verify=False).json()["target_id"]

        return target_id

    def delete_target(self, target_id):
        '''
        删除target，接收一个参数target_id
        :param target_id: 要删除目标的target_id
        :return: None
        '''
        logger.info("delete target" + target_id)
        api_url = f'{self.url}/api/v1/targets/{target_id}'
        requests.delete(api_url, headers=self.headers, verify=False)


    def create_scan(self, target_id, profile_id="Full_Scan"):
        '''
        新建一个扫描，接受两个参数，target_id，profile_id。
        :param target_id: 目标target_id
        :param profile_id: 扫描类型，默认为Full_Scan，支持Full_Scan、High_Risk_Vulnerabilities、Cross_site_Scripting_Vulnerabilities、SQL_Injection_Vulnerabilities、Weak_Passwords、Crawl_Only、Malware_Scan
        :return:None
        '''
        profile_ids = {
            "Full_Scan": "11111111-1111-1111-1111-111111111111",  # 完全扫描
            "High_Risk_Vulnerabilities": "11111111-1111-1111-1111-111111111112",  # 高风险漏洞
            "Cross_site_Scripting_Vulnerabilities": "11111111-1111-1111-1111-111111111116",  # XSS漏洞
            "SQL_Injection_Vulnerabilities": "11111111-1111-1111-1111-111111111113",  # SQL注入漏洞
            "Weak_Passwords": "11111111-1111-1111-1111-111111111115",  # 弱口令检测
            "Crawl_Only": "11111111-1111-1111-1111-111111111117",  # Crawl Only
            "Malware_Scan": "11111111-1111-1111-1111-111111111120",  # 恶意软件扫描
        }
        api_url = f'{self.url}/api/v1/scans'
        values = {
            "target_id": target_id,
            "profile_id": profile_ids[profile_id],
            "schedule": {
                "disable": False,
                "start_date": None,
                "time_sensitive": False
            }
        }
        data = json.dumps(values)
        requests.post(api_url, data, headers=self.headers, verify=False).json()

    def get_all_scans_info(self):
        '''
        :param c:
        :param l:
        :return:
        '''
        api_url = f'{self.url}/api/v1/scans'
        params = (("c", 0), ("l", 1))
        r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
        count = r["pagination"]["count"]
        num = int(int(count) / 100) + 1
        scans = []
        for i in range(num):
            params = (("c", i * 100), ("l", 100))
            tmp_scans = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()["scans"]
            for scan in tmp_scans:
                tmp = {
                    "scan_session_id": scan['current_session']['scan_session_id'],
                    "severity_counts": scan['current_session']['severity_counts'],
                    "start_date": scan['current_session']['start_date'],
                    "status": scan['current_session']['status'],
                    "scan_id": scan['scan_id'],
                    "address": scan['target']['address'],
                    "description": scan['target']['description'],
                    "target_id": scan['target_id'],
                }
                print(tmp)
                scans.append(tmp)
        return scans

    def get_scans_info_by_target_id(self, target_id):
        '''
        根据关键字获取特定的扫描信息，主要包含以下字段：targets（目标详细信息）、pagination（分页信息
        :return:dict
        '''
        params = (("q", f"target_id:{target_id};"),)
        api_url = f'{self.url}/api/v1/scans'
        tmp = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()["scans"][0]

        scan = {
            "scan_session_id": tmp['current_session']['scan_session_id'],
            "severity_counts": tmp['current_session']['severity_counts'],
            "start_date": tmp['current_session']['start_date'],
            "status": tmp['current_session']['status'],
            "scan_id": tmp['scan_id'],
            "address": tmp['target']['address'],
            "description": tmp['target']['description'],
            "target_id": tmp['target_id'],
        }
        return scan

    def delete_scan(self, scan_id):
        logger.info("delete scan" + scan_id)
        api_url = f'{self.url}/api/v1/scans/{scan_id}'
        requests.delete(api_url, headers=self.headers, verify=False)

    def get_scan_result_info(self, scan_id, scan_session_id):
        api_url = f'{self.url}/api/v1/scans/{scan_id}/results/{scan_session_id}/statistics'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        result_info = {
            "start_date": r["scanning_app"]["wvs"]["start_date"],
            "end_date": r["scanning_app"]["wvs"]["end_date"],
            "status": r["status"],
            "severity_counts": r["severity_counts"]
        }
        return result_info

    def get_scan_result_vulnerabilities(self, scan_id, scan_session_id, count=100):
        vulnerabilities = []
        api_url = f'{self.url}/api/v1/scans/{scan_id}/results/{scan_session_id}/vulnerabilities?l=1&s=severity:desc'
        count = requests.get(url=api_url, headers=self.headers, verify=False).json()["pagination"]["count"]
        num = int(int(count) / 100) + 1
        for i in range(num):
            api_url = f'{self.url}/api/v1/scans/{scan_id}/results/{scan_session_id}/vulnerabilities?l={100}&s=severity:desc'
            tmp_vulnerabilities = requests.get(url=api_url, headers=self.headers, verify=False).json()[
                "vulnerabilities"]
            for tmp_vulnerabilitie in tmp_vulnerabilities:
                vulnerabilities.append({
                    "confidence": tmp_vulnerabilitie["confidence"],
                    "vt_id": tmp_vulnerabilitie["vt_id"],
                    "vt_name": tmp_vulnerabilitie["vt_name"],
                    "vuln_id": tmp_vulnerabilitie["vuln_id"],
                })
        return vulnerabilities

    def get_scan_vulnerabilitie_info(self, scan_id, scan_session_id, vuln_id):
        api_url = f'{self.url}/api/v1/scans/{scan_id}/results/{scan_session_id}/vulnerabilities/{vuln_id}'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        if r["severity"] == "0":
            severity = "信息性"
        elif r["severity"] == "1":
            severity = "低危"
        elif r["severity"] == "2":
            severity = "中危"
        elif r["severity"] == "3":
            severity = "高危"
        else:
            severity = None
        vulnerabilitie_info = {
            "vt_name": r["vt_name"],
            "vuln_description": r["description"],
            "confidence": r["confidence"],
            "cvss_score": r["cvss_score"],
            "details": r["details"],
            "impact": r["impact"],
            "recommendation": r["recommendation"],
            "request": r["request"],
            "vt_id": r["vt_id"],
            "severity": severity,
            "vuln_id": r["vuln_id"]
        }
        return vulnerabilitie_info

    def get_vulnerabilitie_info(self, vuln_id):
        api_url = f'{self.url}/api/v1/vulnerabilities/{vuln_id}'
        r = requests.get(url=api_url, headers=self.headers, verify=False).json()
        print(r)
        if r["severity"] == "0":
            severity = "信息性"
        elif r["severity"] == "1":
            severity = "低危"
        elif r["severity"] == "2":
            severity = "中危"
        elif r["severity"] == "3":
            severity = "高危"
        else:
            severity = None
        vulnerabilitie_info = {
            "vt_name": r["vt_name"],
            "vuln_description": r["description"],
            "confidence": r["confidence"],
            "cvss_score": r["cvss_score"],
            "details": r["details"],
            "impact": r["impact"],
            "recommendation": r["recommendation"],
            "request": r["request"],
            "vt_id": r["vt_id"],
            "severity": severity,
            "vuln_id": r["vuln_id"]
        }
        return vulnerabilitie_info

    def get_scan_vulnerabilities_by_domain(self, domain):
        vulnerabilities = []
        target_info = self.get_targets_info_by_key_word(domain)[0]
        sacn_info = self.get_scans_info_by_target_id(target_info["target_id"])
        target_scan_result = self.get_scan_result_info(sacn_info["scan_id"], sacn_info["scan_session_id"])
        tmp_vulnerabilities = self.get_scan_result_vulnerabilities(sacn_info["scan_id"], sacn_info["scan_session_id"])
        for vulnerabilitie in tmp_vulnerabilities:
            vulnerabilitie_info = self.get_scan_vulnerabilitie_info(sacn_info["scan_id"], sacn_info["scan_session_id"],
                                                                    vulnerabilitie["vuln_id"])
            vulnerabilities.append(vulnerabilitie_info)
        result = {
            "address": target_info["address"],
            "description": target_info["description"],
            "severity_counts": sacn_info["severity_counts"],
            "start_date": target_scan_result["start_date"],
            "end_date": target_scan_result["end_date"],
            "status": target_scan_result["status"],
            "vulnerabilities": vulnerabilities
        }
        return result

    def delete_target_according_key_word(self, key_word):
        '''
        根据关键字删除对应的targe信息。返回已经删除的target列表。
        :param key_word: 要删除的target的关键字
        :return: list
        '''
        '''
        删除target，接收一个关键字。
        :return:list
        '''
        print("3333")
        delete_targets = []
        for target in self.get_targets_info_by_key_word(key_word):
            address = target["address"]
            description = target["description"]
            target_id = target["target_id"]
            self.delete_target(target_id)
            delete_targets.append({"address": address,
                                   "description": description,
                                   "target_id": target_id})
            try:
                scan_id = self.get_scans_info_by_target_id(target_id)
                self.delete_scan(scan_id)
            except:
                pass
        return delete_targets

    def get_all_targets_info(self):
        '''
        获取AWVS中存在的所有target信息，返回list数据，其中每个目标的信息组合成一个字典，包含address、address、target_id信息。
        :return: list
        '''
        targets = []
        api_url = f'{self.url}/api/v1/targets'
        params = (("c", 0), ("l", 1))
        r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
        count = r["pagination"]["count"]
        num = int(int(count) / 100) + 1
        for i in range(num):
            params = (("c", i * 100), ("l", 100))
            api_url = f'{self.url}/api/v1/targets'
            r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
            tmp_targets = r["targets"]
            for target in tmp_targets:
                tmp = {"address": target["address"],
                       "description": target["description"],
                       "target_id": target["target_id"]}
                print(tmp)
                targets.append(tmp)
        return targets

    def get_all_vulnerabilities(self):
        api_url = f'{self.url}/api/v1/vulnerability_types'
        params = (
            ('c', '0'),
            ('l', '1'),
            ('q', 'status:open;'),
        )
        vulnerabilities = []
        r = requests.get(api_url, headers=self.headers, params=params, verify=False).json()
        count = r["pagination"]["count"]
        num = int(int(count) / 100) + 1
        for i in range(num):
            params = (
                ('c', i * 100),
                ('l', '100'),
                ('q', 'status:open;'),
            )
            vulnerability_types = requests.get(api_url, headers=self.headers, params=params, verify=False).json()[
                "vulnerability_types"]
            for vulnerability_type in vulnerability_types:
                name = vulnerability_type["name"]
                vt_id = vulnerability_type["vt_id"]
                count = vulnerability_type["count"]
                if vulnerability_type["severity"] == "0":
                    severity = "信息性"
                elif vulnerability_type["severity"] == "1":
                    severity = "低危"
                elif vulnerability_type["severity"] == "2":
                    severity = "中危"
                elif vulnerability_type["severity"] == "3":
                    severity = "高危"
                else:
                    severity = None
                params = (
                    ('l', '100'),
                    ('q', f'status:open;vt_id:{vt_id};')
                )
                tmp_vulnerabilities = \
                    requests.get(f'{self.url}/api/v1/vulnerabilities', headers=self.headers, params=params,
                                 verify=False).json()["vulnerabilities"]
                # if name =="SQL 注入":
                vulnerabilitie = []
                for tmp_vulnerabilitie in tmp_vulnerabilities:
                    vulnerabilitie.append(tmp_vulnerabilitie["vuln_id"])
                vulnerabilities.append({
                    "name": name,
                    "count": count,
                    "severity": severity,
                    "vulnerabilities": vulnerabilitie
                })
        return vulnerabilities

    def create_target_and_scan(self, target, description):
        logger.info(f"正在将{description}:{target}添加到awvs进行扫描。")
        try:
            target_id = self.create_target(target, description)
        except:
            logger.error(f"添加{target}失败")
        try:
            self.create_scan(target_id)
        except:
            logger.error(f"添加{target}扫描失败")

    def clean_all_scan_target(self):
        api_url = f'{self.url}/api/v1/targets'
        params = (("c", 0), ("l", 1))
        r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
        count = r["pagination"]["count"]
        num = int(int(count) / 100) + 1
        for i in range(num):
            params = (("c", 0), ("l", 100))
            api_url = f'{self.url}/api/v1/targets'
            try:
                r = requests.get(url=api_url, headers=self.headers, params=params, verify=False).json()
                tmp_targets = r["targets"]
                print(tmp_targets)
                for target in tmp_targets:
                    target_id = target["target_id"]
                    scan_id = self.get_scans_info_by_target_id(target_id)["scan_id"]

                    self.delete_scan(scan_id)

                    self.delete_target(target_id)
            except Exception as e:
                logger.error(e)


AWVS_URL = globals.get_value("AWVS_URL")
AWVS_API_KEY = globals.get_value("AWVS_API_KEY")
awvsapi = AwvsApi(AWVS_URL, AWVS_API_KEY)
