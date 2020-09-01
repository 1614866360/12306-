#coding:utf-8

import requests
import urllib3
import json
from prettytable import PrettyTable
import stations

from tkinter import *
import sqlite3


def SS(): #该自定义函数在创建子窗体，实现库内查询功能
    newwin = Toplevel(master= root)
    var1=StringVar()
    var2=StringVar()
    var3=StringVar()
    checkvar1=StringVar()
    checkvar2=StringVar()
    checkvar3=StringVar()
    checkvar4=StringVar()
    checkvar5=StringVar()
    #定义StringVar()变量便于取出输入框，复选框的值
    newwin.title('库内查询')
    newwin.geometry('800x600')
    text1= Text(newwin)
    #接下来定义各个控件并放在子窗体上
    lb1 = Label(newwin,text='日期:(xxxx-xx-xx)')
    inp1 = Entry(newwin,textvariable=var1)
    lb2 = Label(newwin,text='始发站:')
    inp2 = Entry(newwin,textvariable=var2)
    lb3 = Label(newwin,text='终点站:')
    inp3 = Entry(newwin,textvariable=var3)
    lb1.place(relx=0,relwidth=0.2,rely=0,relheight=0.2)
    inp1.place(relx=0.17,relwidth=0.15,rely=0.05,relheight=0.1)
    lb2.place(relx=0.4,relwidth=0.1,rely=0.05,relheight=0.1)
    inp2.place(relx=0.5,relwidth=0.1,rely=0.05,relheight=0.1)
    lb3.place(relx=0.6,relwidth=0.1,rely=0.05,relheight=0.1)
    inp3.place(relx=0.7,relwidth=0.1,rely=0.05,relheight=0.1)
    ch1 = Checkbutton(newwin,text='高铁',variable=checkvar1,onvalue ='G',offvalue=None)
    ch2 = Checkbutton(newwin,text='动车',variable=checkvar2,onvalue ='D',offvalue=None)
    ch3 = Checkbutton(newwin,text='快速',variable=checkvar3,onvalue ='K',offvalue=None)
    ch4 = Checkbutton(newwin,text='特快',variable=checkvar4,onvalue ='T',offvalue=None)
    ch5 = Checkbutton(newwin,text='直达',variable=checkvar5,onvalue ='Z',offvalue=None)
    ch1.place(relx=0.31,relwidth=0.1,rely=0,relheight=0.05)
    ch2.place(relx=0.31,relwidth=0.1,rely=0.05,relheight=0.05)
    ch3.place(relx=0.31,relwidth=0.1,rely=0.1,relheight=0.05)
    ch4.place(relx=0.31,relwidth=0.1,rely=0.15,relheight=0.05)
    ch5.place(relx=0.31,relwidth=0.1,rely=0.2,relheight=0.05)
    text1.place(relx=0,relwidth=1,rely=0.25,relheight=0.75)
   
    
    def search(): #该函数实现在库内查询并将查询结果显示在文本框中
        day = var1.get()
        fromW = var2.get()
        toW = var3.get()
        C1= checkvar1.get()
        C2= checkvar2.get()
        C3= checkvar3.get()
        C4= checkvar4.get()
        C5= checkvar5.get()
        #将输入框，复选框内容取出
        conn = sqlite3.connect('12306.db')
        cursor = conn.cursor()
        sql="select* from alldata WHERE 日期= '%s' AND 始发站 LIKE '%%%s%%'AND 终点站 LIKE '%%%s%%' AND \
            (车次 LIKE '%s%%'OR 车次 LIKE '%s%%' OR 车次 LIKE '%s%%' OR 车次 LIKE '%s%%'\
            OR 车次 LIKE '%s%%')" %(day,fromW,toW,C1,C2,C3,C4,C5) #日期使用精确查询，地点使用模糊查询，并筛选用户选择的车次类型
        # sql语句从数据库中查询符合用户输入的条件的所有结果
      
        cursor.execute(sql)
        result = cursor.fetchall()
        resultout = PrettyTable()
        #同样使用 PrettyTable()将结果表格化，美化后输出
        resultout._set_field_names('车次 日期 车站 时间 历时 商务座 一等座  二等座  动卧  软卧   硬卧  硬座 无座'.split())
        for i in result:
            resultout.add_row([i[0],i[1],
                                '\n'.join([i[2],i[3]]),#把站名放在一起
                                '\n'.join([i[4],i[5]]),#把发车时间和到达时间放在一起
                                i[6],i[7],i[8],i[9],
                                i[10],i[11],i[12],
                                i[13],i[14]
                                ])                          #利用prettytable美化，使之输出为表格形式

            
        conn.commit()
        conn.close()
        text1.delete(1.0,END)
        text1.insert(INSERT,resultout)
        

    btn = Button(newwin,text='查询',command=search)
    btn.place(relx=0.85,relwidth=0.15,rely=0.02,relheight=0.1)
    
    btclose = Button(newwin,text='关闭',command=newwin.destroy).place(relx=0.85,relwidth=0.15,rely=0.15,relheight=0.1)



def tickets(entry2,entry3,entry4,entry5):

    global date

    str = entry2.get() #请输入出发站
    str1 =entry3.get() #请输入到达站
    date = entry4.get() #请输入出发日期(格式xxxx-xx-xx)
    options = entry5.get() #请输入列车类型（格式g、d、t、k、z)

    #获取地名对应的简写代码
    from_station = stations.station[str]
    to_station = stations.station[str1]

#   例如：https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-06-19&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT

    #对url进行分析,拿到正确的url
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
           'leftTicketDTO.train_date={}&'
           'leftTicketDTO.from_station={}&'
           'leftTicketDTO.to_station={}&'
           'purpose_codes=ADULT').format(date, from_station, to_station)

    #设置headers
    headers={
        "Cookie":"tk=-tIp2gt3OFnd85DwD1ZPefIm_hqqr_fZ4R8LmgtyT1T0; JSESSIONID=8C879BE703110108760AB7B06D189E4C; _jc_save_wfdc_flag=dc; ten_key=XHg9EqyTtYQzWSFbtdFVvi/EYPgxHIlZ; ten_js_key=XHg9EqyTtYQzWSFbtdFVvi%2FEYPgxHIlZ; ten_join_key=XHg9EqyTtYQzWSFbtdFVvi%2FEYPgxHIlZ%2CXHg9EqyTtYQzWSFbtdFVvi%2FEYPgxHIlZ; _jc_save_toStation=%u4E0A%u6D77%2CSHH; RAIL_EXPIRATION=1592636846009; RAIL_DEVICEID=VBzKZAfI0UiD-1Yb5clAfVIDbU7xbTVZh1yYP4d0A67zrJm_cXcZICUuM4ybvuqHzkOzcI9eCiAaF8VEetB7JdRw6K0UBo1duL5H_CO4KRFq4qqnM4pS3BBgxrAdrY4gadfZ3I5JO8ZXq17sk8UJ2PkpVMizthOp; BIGipServerpassport=988283146.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_toDate=2020-06-19; BIGipServerpool_passport=283968010.50215.0000; BIGipServerotn=921698826.24610.0000; _jc_save_fromStation=%u5357%u4EAC%u5357%2CNKH; _jc_save_fromDate=2020-06-20"
    }

    r = requests.get(url,headers=headers, verify=False)
    r=r.text

    # requests得到的是一个json格式的对象，利用json转化成python字典格式数据来提取
    j=json.loads(r)

    global raw_trains #定义全局变量，在导入数据库函数中使用
    raw_trains = j['data']['result']#提取J中的“data”和“result”数据

    x = PrettyTable()

    x._set_field_names('车次 车站 时间 历时 商务座 一等座  二等座  动卧  软卧   硬卧  硬座 无座'.split())#得到信息的列表
    for raw_train in raw_trains:
        
        data_list = raw_train.split('|')#由于在raw_train 中分隔符为“|”，故用此将信息隔开
        
        train_number = data_list[3]         #获取列车编号
        initial = train_number[0].lower()   #由于在raw_train 中列车类型首字母均为大写，例如“G5”，为了和开始我们的信息的填写相对应，我们这里进行大小写转换

        if not options or initial in options: #如果没有options（此时不做判断全部输出） 或者 列车首字母小写在options内则输出
            #获取对应信息
            from_station_code = data_list[6]    #出发站简写代码
            to_station_code = data_list[7]      #终点站简写代码

            from_station_name = ''              #这里给它设置为空值，后面用简写代码加上
            to_station_name = ''

            start_time = data_list[8]           #出发时间
            arrive_time = data_list[9]          #到达时间
            time_duration = data_list[10]       #历时
            business_seat = data_list[32] or '--'   #商务座，如果数据为空返回“--”
            first_class_seat = data_list[31] or '--'    #一等座
            second_class_seat = data_list[30] or '--'   #二等座
            pneumatic_sleep = data_list[33] or '--'     #动卧
            soft_sleep = data_list[23] or '--'          #软卧
            hard_sleep = data_list[28] or '--'          #硬卧
            hard_seat = data_list[29] or '--'           #硬座
            no_seat = data_list[26] or '--'             #无座
            x.add_row([train_number,
                        '\n'.join([stations.get_name(from_station_code), stations.get_name(to_station_code)]),#把站名放在一起
                        '\n'.join([start_time, arrive_time]),#把发车时间和到达时间放在一起
                        time_duration,
                        business_seat,
                        first_class_seat,
                        second_class_seat,
                        pneumatic_sleep,
                        soft_sleep,
                        hard_sleep,
                        hard_seat,
                        no_seat
                        ])                          #利用prettytable美化一下，使之输出为表格形式

    #这里用tkinter展示
    
    global root
    root= Tk()
    root.geometry("800x600")
    root.title("列车时刻表")
    text =Text(root, width=800, height=500)
    btn1 =Button(root,text='导入数据库',command=leadin) #按钮一将数据导入数据库
    btn2 =Button(root,text='到库内查询',command=SS) #按钮二执行自定义SS函数
    text.place(relx=0,relwidth=0.9,rely=0,relheight=1)
    btn1.place(relx=0.9,relwidth=0.1,rely=0.4,relheight=0.2)
    btn2.place(relx=0.9,relwidth=0.1,rely=0.6,relheight=0.2)
    text.insert(INSERT, x)
    root.mainloop()

def leadin(): #自定义将数据导入数据库的函数
        conn = sqlite3.connect('12306.db') #建立与数据库的连接
        cursor = conn.cursor() #使用游标进行操作
        SQL1 ='''create table if not exists alldata(车次,日期,始发站,终点站,出发时间,到达时间,历时,
            商务座,一等座,二等座,动卧,软卧,硬卧,硬座,无座,PRIMARY KEY(车次,日期))'''
        # SQL1语句在数据库内创建一张表（如果已经存在则不再创建），以车次，日期作为主键
        cursor.execute(SQL1) #执行SQL1语句
        conn.commit() #递交执行结果
        for raw_train in raw_trains:    #用循环将车次信息以列表导入数据库
            data_list = raw_train.split('|')
            SQL2 ='''insert or replace into alldata (车次,日期,始发站,终点站,出发时间,到达时间,历时,
            商务座,一等座,二等座,动卧,软卧,硬卧,硬座,无座) values('%s','%s','%s','%s','%s','%s','%s','%s',
            '%s','%s','%s','%s','%s','%s','%s')'''%(data_list[3],date,stations.get_name(data_list[6]),
            stations.get_name(data_list[7]),data_list[8],data_list[9],data_list[10],data_list[32],
            data_list[31],data_list[30],data_list[33],data_list[23],data_list[28],data_list[29],data_list[26]) 
            #以车次，日期为主键判断是否存在，不存在则插入，存在则更新
            cursor.execute(SQL2)
            conn.commit()
        conn.close()



if __name__ == '__main__':
    tickets()
    



