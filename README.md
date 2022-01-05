# 功能简介

通过输入的关键字（企业名称，域名，ip，其他关键字）进行信息收集，而后对收集到的信息进行整理及二次收集（子域名，C段），而后调用三方工具（awvs，xray，hydra，vulmap）进行测试。

具体流程如下:

1. 根据`公司名称`或`关键字`调用`天眼查`或`企查查`收集相关`主域名`。

2. 根据`主域名`调用`oneforall`收集`子域名`及对应`ip地址`。
3. 根据`ip地址`调用`fofa`、`zoomeye`、`360Quake`、`dismap`、`infoscan`对相关`ip地址`或`网段`进行扫描发现相关的`服务`。
4. 根据`服务`调用`Awvs`、`hydra`、`Xray`、`Vulmap`进行扫描发现存在的漏洞。
5. 根据`扫描结果`，进行验证测试。

每一步测试的数据，即可以根据上一步测试生成，也可以由自己主动输入。可以根据实际情况自主选择搭配。

# 使用

需要下载第三方工具并添加到tools文件夹下，已上传百度云。

>链接：https://pan.baidu.com/s/1mJxJxBnAKz0Evb2wuDB5Qw 
>提取码：yc13

而后配置conf目录下的config.py。

注意：

> hydra需要自己下载并配置环境变量

# 参数

```
usage: python3 xiaobai [options]

optional arguments:
  -h, --help            show this help message and exit

target:
  you must to specify target

  --ip IP               target ip (e.g. --ip "8.8.8.8")
  --ipfile IPFILE       select a ip list file (e.g. --ipfile"list.txt")
  --cidr CIDR           set network cidr (e.g. --cidr 24)
  --domain DOMAIN       target domain (e.g. --domain "baidu.com")
  --domainfile DOMAINFILE
                        select a domain list file (e.g. --domainfile"list.txt")
  --company COMPANY     company (e.g. --domain "baidu.com")
  --companyfile COMPANYFILE
                        select a companyfile list file (e.g. --domainfile"list.txt")
  --keyword KEYWORD     target keyword (e.g. --keyword "阿里巴巴")
  --keywordfile KEYWORDFILE
                        select a keyword list file (e.g. --keywordfile"list.txt")
  --url URL             target url (e.g. --url "http://www.baidu.com")
  --title TITLE         url title (e.g. --title "http://www.baidu.com")
  --urlfile URLFILE     select a url list file (e.g. --keywordfile"list.txt")
  --noping              ping or not
  --filter FILTER       filter keyword search result (e.g. --filter "{'主办单位性质':'个人,事业单位'}")

scans:
  options vulnerability scanning or exploit mode

  --ipsearch IPSEARCH   Choose need to search the IP module, support the use of multiple modules at the same time,split with ',' ,support [fofa, zoomeye, 360, shodan dismap](e.g.
                        --ipsearch fofa,360)
  --vulscan VULSCAN     Select the modules that need to be scanned for vulnerability, support the use of multiple modules at the same time, split with ',',support [awvs, xray,
                        vulmap,hydra](e.g. --vulscan awvs,vulmap)

examples:
  python3 xiaobai.py --keyword XX --filter {\"主办单位性质\":\"政府,事业单位\"} --ipsearch fofa --vulscan awvs --cidr 32
  python3 xiaobai.py --ip XXX.XXX.XXX.XXX --ipsearch fofa --vulscan hydra --cidr 24
  python3 xiaobai.py --company 阿里巴巴 --ipsearch fofa --vulscan vulmap --cidr 32
  python3 xiaobai.py --keywordfile keywords.txt --ipsearch fofa --cidr 28 --vulscan vulmap,awvs,hydra
```

# 结果

结果保存到results文件夹下，每次使用会清空上一次结果，如需要保存，需手动复制到其他位置。

