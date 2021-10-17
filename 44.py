from ctypes import resize
from io import BytesIO

import tkinter

from PIL import ImageTk
from scapy.all import *

from tkinter import *
from colorama import Cursor
from scapy.contrib.isotp import scan





def dosniff(filter_rule,sniff_time,prn_f):
    sniff(filter=filter_rule,timeout=sniff_time,prn=prn_f) # 监听数据包

def handlepacket(p):
    global N,img_list,imgvalue_list,img_map
    if p.haslayer(Raw): # 找出有上网数据的
        load = p.load
        ack = p.ack
        try:
            ## 如果为图片相应,且带有HTTP头(即第一个图片TCP包)
            if 'Content-Type: image' in str(load): # 如果为图片响应
                postfix = re.findall('image/(.*?)\\\\r',str(load))[0] # 图片后缀
                length = int(re.findall('Content-Length: (.*?)\\\\r',str(load))[0]) # 图片数据长度
                ip_src = p['IP'].src # 源头IP
                ip_dst = p['IP'].dst # 目的IP
                img_list[ack] = [(postfix,length,ip_src,ip_dst)] # 0为图片信息(以下为图片二进制数据)
                img_load=load[load.find(b'\x0d\x0a\x0d\x0a')+4:] # 去除请求头部分，只要图片数据
                img_list[ack].append(img_load)
            ## 如果为某图片的后续数据包
            elif ack in list(img_list.keys()):
                img_load = load # 所有load均为图片数据
                img_list[ack].append(img_load)
                img = bytes()
                postfix = img_list[ack][0][0] # 图片后缀
                length = img_list[ack][0][1] # 图片长度
                ip_src = img_list[ack][0][2] # 源头IP
                ip_dst = img_list[ack][0][3] # 目的IP
                for i in img_list[ack][1:]:
                    img += i
                if len(img) == length: # 如果图片数据已经完整
                    imgname = '%d.%s'%(N,img_map[postfix])
                    with open('./images/%s/%s'%(target,imgname),'wb') as f:
                        f.write(img)
                        img = Image.open(BytesIO(img))
                        img = resize(200,200,img)
                        img_tk = ImageTk.PhotoImage(img)
                        imgvalue_list.append(img_tk)
                        Label(frame,image=imgvalue_list[-1],bg='black').grid(row=(N-1)//4,column=(N-1)%4,padx=23,pady=3)
                        canvas.create_window((ww/2,math.ceil(N/4)*105), window=frame)  #create_window
                        canvas['scrollregion'] = (0,0,ww,math.ceil(N/4)*210)
                        canvas.yview_moveto(1)
                        print('%s【driftnet】: saving image data as "%s"'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),imgname))
                        N += 1
        except:
            pass


# 主函数

def stop_thread(t):
    pass


def printinfo():
    pass


if __name__ == '__main__':
    printinfo()
    colored = Cursor
    target = ''
    sniff_time = 24 * 60 * 60

    while True:
        choice = input('\n请选择:')
        if choice not in ['1', '2', '3', '4', '5']:
            print(colored('>>>选择错误，请重新输入!', 'red'))
            time.sleep(1)
            printinfo()
        else:
            if choice == '1':
                scan()
            if choice == '2':
                target = input('>>>监听目标(对方IP地址):')
                print('监听目标设置成功!')
                time.sleep(1)
                printinfo()
            if choice == '3':
                sniff_time = input('>>>监听时间(默认为86400秒):')
                sniff_time = int(sniff_time)
                print('监听时间设置成功!')
                time.sleep(1)
                printinfo()
            if choice == '4':
                if target == '':
                    print(colored('监听目标未设置!', 'red'))
                    time.sleep(1)
                    printinfo()
                else:
                    print(f'监听目标为"{target}"  监听时间为"{sniff_time}秒"' )
                    op = input('是否开始(Y/N)?')
                    if not (op == 'Y' or op == 'y'):
                        printinfo()
                        continue
                    # 创建GUI
                    ## 初始化全局变量
                    N = 1  # 图片编号
                    img_list = {}  # 图片字典,用于存储图片信息，以及对应数据包
                    imgvalue_list = []  # 图片数据，用于在画布上显示(防止由于局部变量等原因丢失变量)
                    ## 相关参数
                    bgcolor = 'black'
                    ## 创建root窗口(1000x630)
                    root = Tk()
                    root.title('driftnet')  # 设置标题
                    # root.iconbitmap('logo.ico')
                    root.config(bg=bgcolor)
                    sw = root.winfo_screenwidth()  # 屏幕宽度
                    sh = root.winfo_screenheight()  # 屏幕高度
                    ww = 1000  # 窗口宽度
                    wh = 630  # 窗口高度
                    x = (sw - ww) / 2  # 窗口横坐标
                    y = (sh - wh) / 2  # 窗口纵坐标
                    root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
                    root.resizable(width=False, height=False)  # 窗口大小无法更改
                    ## 创建画布canvas
                    canvas = Canvas(root, width=ww, height=wh)  # 创建canvas
                    canvas.grid()
                    ## 创建frame窗口
                    frame =  tkinter.Frame(canvas)
                    frame.grid()
                    ## 滚动条
                    vbar = Scrollbar(root, orient=VERTICAL)  # 竖直滚动条
                    vbar.place(x=ww - 20, y=0, width=20, height=wh)
                    vbar.configure(command=canvas.yview)
                    canvas.config(yscrollcommand=vbar.set)  # 设置

                    # 嗅探数据
                    if not os.path.exists('./images'):
                        os.mkdir('./images')
                    if not os.path.exists('./images/%s' % target):
                        os.mkdir('./images/%s' % target)
                    filter_rule = "tcp src port 80 and dst host {}".format(target)  # 过滤规则
                    print('开始嗅探.....')
                    t = threading.Thread(target=dosniff, args=(filter_rule, sniff_time, handlepacket,))
                    t.start()

                    # 进入消息循环
                    root.mainloop()

                    # 关闭嗅探线程
                    stop_thread(t)
                    # input() # 处理stop_thread多余的输出流
                    printinfo()
            if choice == '5':
                print('Good bye!')
                exit(0)