from tkinter import *
import os
import login
import tickets

root=Tk()
root.title('12306查询')
photo=PhotoImage(file='bg.gif')
label=Label(root,text='欢迎进入本程序，我们将为你提供最优质的服务',
               justify=LEFT,
               image=photo,
               font=('华文新魏',10),
               compound=CENTER)#添加背景
label.pack()


def cxjm():
    root2=Tk()
    root2.geometry('480x640')
    root2.title('12306查询')
    photo=PhotoImage(file='bg.gif')
    label2=Label(root2,text='******')
    label2.pack()
    label3=Label(root2,text='起始站:')#输入起始站
    label3.place(relx=0.1,rely=0.1)
    inp1=Entry(root2)
    inp1.place(relx=0.3,rely=0.1,relwidth=0.3)
    label4=Label(root2,text='终点站:')#输入终点站
    label4.place(relx=0.1,rely=0.2)
    inp2=Entry(root2)
    inp2.place(relx=0.3,rely=0.2,relwidth=0.3)
    label5=Label(root2,text='出发时间：')#输入出发时间
    label5.place(relx=0.1,rely=0.3)
    inp3=Entry(root2)
    inp3.place(relx=0.3,rely=0.3,relwidth=0.3)
    label6=Label(root2,text='列车类型')#输入列车类型
    label6.place(relx=0.1,rely=0.4)
    inp4=Entry(root2)
    inp4.place(relx=0.3,rely=0.4,relwidth=0.3)
    label0=Label(root2,text='查询须知:\nd----动车\ng----高铁\nk----快速\nt----特快\nz----直达\n日期格式:\n20**-**-**')#查询须知
    label0.place(relx=0.8)

    btn_1=Button(root2,text='查询',command=lambda:tickets.tickets(inp1,inp2,inp3,inp4))#一键查询，f2为查询函数
    btn_1.place(relx=0.25,rely=0.5)


def drjm():
    root3=Tk()
    root3.geometry('480x640')
    lb1=Label(root3,text='用户名:')#登入界面
    lb1.place(relx=0.1,rely=0.2)
    inp_1=Entry(root3)
    inp_1.place(relx=0.3,rely=0.2,relwidth=0.3)
    lb2=Label(root3,text='密码:')
    lb2.place(relx=0.1,rely=0.4)
    inp_2=Entry(root3,show='*')
    inp_2.place(relx=0.3,rely=0.4,relwidth=0.3)
    #btn=Button(root3,text='登录',command=lambda:login.loginTo(inp_yzm,inp_1,inp_2))#暂未解决登入界面
    btn=Button(root3,text='登录',command=cxjm)
    btn.place(relx=0.3,rely=0.5)


def next_button():
    xyb=Button(root,text='下一步',command=drjm)
    xyb.place(relx=0.3,rely=0.6)


# def cxjg():#此处添加查询结果
#     root3=Tk()
#     root3.title('查询结果')
#     root3.geometry('480x640')
#     lbl=Label(root3,text='查询结果')
#     lbl.pack()


yzm_1=Button(root,text='获取验证码',command=login.getImg)#获取验证码
yzm_1.place(relx=0.2,rely=0)
yzm_2=Label(root,text='请输入验证码位置(横向编排，从0到7)，以","分割[例如2,5]:')
yzm_2.place(relx=0,rely=0.1)
inp_yzm=Entry(root)
inp_yzm.place(relx=0,rely=0.2)
yzm_3=Button(root,text='点击验证',command=lambda:login.check_yanzheng(inp_yzm,next_button))#验证

yzm_3.place(relx=0.2,rely=0.3)

#-----------------------------------------------

def jubao():
    s='举报'
    label.config(text=s)
    f=open('举报.txt','r')
    for line in f:
        print(line,end='')
    f.close()

def popupmenu(event):
    mainmenu.post(event.x_root,event.y_root)
#-----------------------------------------------

mainmenu=Menu(root)
menufile=Menu(mainmenu)
mainmenu.add_command(label='举报',command=jubao)#设置举报键


root.config(menu=mainmenu)
root.bind('<Button-3>',popupmenu)
root.mainloop()
