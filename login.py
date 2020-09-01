import requests

from PIL import Image

from json import loads

import tkinter

import tkinter.messagebox

import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning

#------------------------------------------------------------------------------------

#禁用安全请求警告

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   

#构造请求头

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
           "host": 'kyfw.12306.cn',
           "Origin": "https://kyfw.12306.cn",
           'Referer': "https://kyfw.12306.cn/otn/resources/login.html",
           }

# 创建一个网络请求session实现登录验证

session = requests.Session()

url = 'https://kyfw.12306.cn/otn/resources/login.html'

session.get(url)

#------------------------------------------------------------------------------------

# 获取验证码图片

def getImg():

    captcha_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"

    #构造请求表
    params = {
        'login_site':"E",
        
        'module':"login",
        
        'rand':	"sjrand",
        
        '1592066730045':"",
        
        'callback':"jQuery191008726783928441906_1592066728574",
        
        '_':"1592066728575"
                }
    
    #用session.get获取验证图片的页面
    
    response = session.get(url=captcha_url, params=params, headers=headers)

    # 把验证码图片保存到本地

    with open('img.jpg','wb') as f:

        f.write(response.content)

    im = Image.open('img.jpg')

    # 展示验证码图片，会调用系统自带的图片浏览器打开图片

    im.show()

    # 关闭，只是代码关闭，实际上图片浏览器没有关闭

    im.close()

#------------------------------------------------------------------------------------

def check_yanzheng(entry1,next_button):
    
    #调用获取验证码函数，得到输入后的验证码位置
    
    yanzheng = entry1.get()
    
    #按，分离成列表
    
    soList = yanzheng.split(',')

    # 由于12306官方验证码是验证正确验证码的坐标范围,取每个验证码中点的坐标(大约)

    yanSol = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']

    yanList = []

    for item in soList:

        yanList.append(yanSol[int(item)])

    # 正确验证码的坐标拼成字符串，作为网络请求时的参数

    yanStr = ','.join(yanList)

    #验证码验证的url

    check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    
    #构建请求参数
    
    parameters = {
        'callback':"jQuery191008726783928441906_1592066728574",
        
        'answer':yanStr,
        
        'rand':"sjrand",
        
        'login_site':"E",
        
        '_':"1592066728576"
                }

    #获取验证结果response，并用正则表达式取出验证结果,并用loads函数将json格式的response转换成字典
    
    check_response = session.get(check_captcha_url, params=parameters)

    check_json = re.findall(r"\((.*?)\)", check_response.text)
    
    check_json_str = check_json[0]
    
    check_json_dict = loads(check_json_str)

    #输出验证结果

    if check_json_dict['result_code']!='4':

        tkinter.messagebox.showinfo('验证结果','验证码校验失败！')
        
        exit

    else:
        
        tkinter.messagebox.showinfo('验证结果','验证码校验成功，请进行账号密码登录！')
        next_button()

#------------------------------------------------------------------------------------

#发送登录请求的方法

def loginTo(entry1,entry2,entry3):

    # 用户输入用户名，这里可以直接给定字符串

    userName = entry2.get()

    # 用户输入密码，这里也可以直接给定

    pwd = entry3.get()

    #再次获取刚刚输入的验证码
    
    yanzheng = entry1.get()
    
    soList = yanzheng.split(',')

    yanSol = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']

    yanList = []

    for item in soList:

        yanList.append(yanSol[int(item)])

    yanStr = ','.join(yanList)

    #构造请求表

    login_url = "https://kyfw.12306.cn/passport/web/login"

    data = {
        
            'username':userName,

            'password':pwd,

            'appid':'otn',
            
            'answer':yanStr

            }

    result = session.post(url=login_url,data=data,headers=headers,verify=False)

    #dic2 = loads(result.content)

    #print(result)
    
    #print('\n\n')
    
    #print(result.content)

    #print(dic2)

#------------------------------------------------------------------------------------

if __name__ == '__main__':

    getImg()

    check_yanzheng()
    
    loginTo()


