import requests
import tldextract
class IcPApi:
    def get_domain(self,url):
        return tldextract.extract(url).domain+'.'+tldextract.extract(url).suffix
    def get_ipc_info(self,url):
        api_url="https://api.oick.cn/icp/api.php"
        data={"url":self.get_domain(url)}
        result=requests.get(api_url,params=data).text
        print(result)



