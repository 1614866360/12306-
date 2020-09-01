# coding=gbk
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)     #忽略证书警告

#站点名称和简写代码的url
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'

r = requests.get(url, verify=False)        # 提取网页信息，不判断证书

pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'  # 正则表达式提取中文以及大写英文字母

result = re.findall(pattern, r.text)       # 进行所需要的信息的提取(列表)

station = dict(result)                     # 转化为字典格式

names_dict=station.keys()                   #提取station中的keys：城市名
telecodes_dict=station.values()             #提取station中的values：城市代码


names=list(station.keys())  #字典转换为列表
telecodes=list(station.values())    #字典转换为列表


#通过代码获取名称
def get_name(telecode):
    try:
        return names[telecodes.index(telecode)]
    except(ValueError, IndexError):
        return None


#通过名称获取代码
def get_telecode(name):
    try:
        return telecodes[names.index(name)]
    except(ValueError, IndexError):
        return None
