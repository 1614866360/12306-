# coding=gbk
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)     #����֤�龯��

#վ�����ƺͼ�д�����url
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'

r = requests.get(url, verify=False)        # ��ȡ��ҳ��Ϣ�����ж�֤��

pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'  # ������ʽ��ȡ�����Լ���дӢ����ĸ

result = re.findall(pattern, r.text)       # ��������Ҫ����Ϣ����ȡ(�б�)

station = dict(result)                     # ת��Ϊ�ֵ��ʽ

names_dict=station.keys()                   #��ȡstation�е�keys��������
telecodes_dict=station.values()             #��ȡstation�е�values�����д���


names=list(station.keys())  #�ֵ�ת��Ϊ�б�
telecodes=list(station.values())    #�ֵ�ת��Ϊ�б�


#ͨ�������ȡ����
def get_name(telecode):
    try:
        return names[telecodes.index(telecode)]
    except(ValueError, IndexError):
        return None


#ͨ�����ƻ�ȡ����
def get_telecode(name):
    try:
        return telecodes[names.index(name)]
    except(ValueError, IndexError):
        return None
