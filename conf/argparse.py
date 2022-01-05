#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse


def arg():
    parser = argparse.ArgumentParser(usage="python3 xiaobai [options]", add_help=False)
    parser.add_argument("-h", "--help", action="help", help="show this help message and exit")
    target = parser.add_argument_group("target", "you must to specify company/ip/domain/keyword")
    target.add_argument("--ip", dest="ip", type=str, help="target ip (e.g. --ip \"8.8.8.8\")")
    target.add_argument("--ipfile", dest="ipfile", help="select a ip list file (e.g. --ipfile \"ipfile.txt\")")
    target.add_argument("--cidr", dest="cidr", help="set network cidr (e.g. --cidr 24)")
    target.add_argument("--domain", dest="domain",  type=str, help="target domain (e.g. --domain \"baidu.com\")")
    target.add_argument("--domainfile", dest="domainfile",  help="select a domain list file (e.g. --domainfile \"domainfile.txt\")")
    target.add_argument("--company", dest="company",  type=str, help="company  (e.g. --company \"阿里巴巴\")")
    target.add_argument("--companyfile", dest="companyfile",  help="select a companyfile list file (e.g. --domainfile \"companyfile.txt\")")
    target.add_argument("--keyword", dest="keyword",  type=str, help="target keyword (e.g. --keyword \"中国\")")
    target.add_argument("--keywordfile", dest="keywordfile",  help="select a keyword list file (e.g. --keywordfile \"keywordfile.txt\")")
    target.add_argument("--url", dest="url",  type=str, help="target url (e.g. --url \"http://www.baidu.com\")")
    target.add_argument("--title", dest="title",  type=str, help=" url title (e.g. --title \"百度\")")
    target.add_argument("--ports", dest="ports", type=str, help="set ports (e.g. --ports \"80,8080\")",default="-")
    target.add_argument("--urlfile", dest="urlfile",  help="select a url list file (e.g. --urlfile \"urlfile.txt\")")
    target.add_argument("--noping", action='store_true', help='ping or not')
    target.add_argument("--filter", dest="filter",  type=str, help="filter keyword search result (e.g. --filter \"{'主办单位性质':'个人,事业单位'}\")")
    mo = parser.add_argument_group("scans", "options vulnerability scanning or exploit mode")
    mo.add_argument("--ipsearch", dest="ipsearch", type=str, help="Choose need to search the IP module, support the use of multiple modules at the same time,split with ',' ,support [fofa, zoomeye, 360, dismap](e.g. --ipsearch fofa,360)")
    mo.add_argument("--vulscan", dest="vulscan", type=str, help="Select the modules that need to be scanned for vulnerability, support the use of multiple modules at the same time, split with ',',support [awvs, xray, vulmap,hydra](e.g. --vulscan awvs,vulmap)")
    example = parser.add_argument_group("examples")
    example.add_argument(action='store_false',
                         dest=r'python3 xiaobai.py --keyword 中国 --filter {\"主办单位性质\":\"个人,事业单位\"} --ipsearch fofa --vulscan awvs --cidr 32'+"\n  "
                              "python3 xiaobai.py --ip XXX.XXX.XXX.XXX --ipsearch fofa --vulscan hydra --cidr 24\n  "
                              "python3 xiaobai.py --company 阿里巴巴 --ipsearch fofa --vulscan vulmap --cidr 32\n  "
                              "python3 xiaobai.py --keywordfile keywords.txt --ipsearch fofa --cidr 28 --vulscan vulmap,awvs,hydra\n  ")
    return parser.parse_args()
