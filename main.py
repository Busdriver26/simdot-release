import simdot as SD
import gifmaker as GM
import os
import imageio
from PIL import Image
import pandas as pd
import numpy as np
INPUT = 'station.txt'
INFOLIB = '.\\infolib\\'
LINE = "line\\"
STATION = "station\\"
STATION_E = "station_e\\" 
GIF = "gif\\"
PNG = "png\\"
PIC = ".\\pic\\"
OFFSET = 23

def strH2F(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        inside_code += 65248
        rstring += chr(inside_code)
    return rstring

def CreateStart(linename,terminal,BW = True,makegif = True):#linename要加路、线,可以不makegif/BW格式
    if linename+terminal+'.gif' in os.listdir(INFOLIB+LINE+GIF):
        print("文件已经存在。")
        return
    STR =  "乘客们,你们好,您现在乘坐的是"+linename+"公交车,方向"+terminal+"."
    if not BW:
        STR =  "乘客们，你们好，您现在乘坐的是"+linename+"公交车，方向"+terminal+"。"
    if linename+terminal+'.png' not in os.listdir(INFOLIB+LINE+PNG):
        SD.DrawSentence(STR,outname = linename+terminal,savepath = INFOLIB+LINE+PNG)
    if makegif:
        image = Image.open(INFOLIB+LINE+PNG+linename+terminal+'.png')
        out = GM.img2gif(image, offset=46, from_='r', has_out=True)
        imageio.mimsave(INFOLIB+LINE+GIF+linename+terminal+'.gif', out , 'GIF', duration=0.05)
    return

def CreateStation(station,makegif = True):
    #超过12个字符的采用滚动gif，否则采用静态gif(if makegif)
    if station+'NEXT.gif' not in os.listdir(INFOLIB+STATION+GIF):
        STR = '下一站  '+station
        pic = SD.DrawSentence(STR,outname = station+'NEXT',savepath =INFOLIB+STATION+PNG, save=True)
        if makegif:
            if len(station)>8:
                image = Image.fromarray(pic)
                out = GM.img2gif(image, offset=46, from_='r', has_out=True)
            else:
                impic = Image.fromarray(pic)
                new =Image.open(PIC+'bkgrnd.png')
                new.paste(impic, (OFFSET*8*(8-len(station)), 0)[::1])
                out = [new]    
            imageio.mimsave(INFOLIB+STATION+GIF+station+'NEXT.gif', out , 'GIF', duration=0.05)
    if station+'ARR.gif' not in os.listdir(INFOLIB+STATION+GIF):
        STR = station+'  到了'
        pic = SD.DrawSentence(STR,outname = station+'ARR',savepath =INFOLIB+STATION+PNG, save=True)
        if makegif:
            if len(station)>9:
                image = Image.fromarray(pic)
                out = GM.img2gif(image, offset=46, from_='r', has_out=True)
            else:
                impic = Image.fromarray(pic)
                new =Image.open(PIC+'bkgrnd.png')
                new.paste(impic, (OFFSET*8*(9-len(station)), 0)[::1])
                out = [new]    
            imageio.mimsave(INFOLIB+STATION+GIF+station+'ARR.gif', out , 'GIF', duration=0.05)

def CreateStation_ENG(station,makegif = True): #英文版到站通知
    #超过12个字符的采用滚动gif，否则采用静态gif
    if station+'NEXT.gif' not in os.listdir(INFOLIB+STATION_E):
        STR = 'Next stop is '+station
        pic = SD.DrawSentence(STR,outname = station+'NEXT',savepath =INFOLIB+STATION_E+PNG, save=True)
        if makegif:
            if len(station)>12:
                image = Image.fromarray(pic)
                out = GM.img2gif(image, offset=46, from_='r', has_out=True)
            else:
                impic = Image.fromarray(pic)
                new =Image.open(PIC+'bkgrnd.png')
                new.paste(impic, (OFFSET*8*(6-len(station)), 0)[::1])
                out = [new]    
            imageio.mimsave(INFOLIB+STATION_E+GIF+station+'NEXT.gif', out , 'GIF', duration=0.05)
    if station+'ARR.gif' not in os.listdir(INFOLIB+STATION_E):
        STR = 'We are arriving at '+ station
        pic = SD.DrawSentence(STR,outname = station+'ARR',savepath =INFOLIB+STATION_E+PNG, save=True)
        if makegif:
            image = Image.fromarray(pic)
            out = GM.img2gif(image, offset=46, from_='r', has_out=True)   
            imageio.mimsave(INFOLIB+STATION_E+GIF+station+'ARR.gif', out , 'GIF', duration=0.05)

def MakeLine(filename=INPUT,eng = False,makegif = True,BW=True):
    '''
    文件格式：
    第一行： 线路名 如 1110路 注意：如果要全角这里在txt里直接打全角
    第二行：终点站1 如 周园路沈梅东路
    第三行：终点站2 如 周浦东站 
    第三行：空
    第四行~第N行：途径站（含终点站）中文
    如果是英文站点信息，请新开一个文件，使filename等于文件名，并把中文站名替换为英文站名，将ENG设置为True。
    '''
    with open(filename, "r",encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if lines[i][-1] == '\n':
            lines[i] = lines[i][:-1]
    L = lines[0]
    start1,start2 = lines[1],lines[2]
    stops = lines[4:]
    print("创建终点站：")
    CreateStart(L,start1,BW=BW,makegif=makegif)
    CreateStart(L,start2,BW=BW,makegif=makegif)
    print("创建站点：")
    if not eng:
        for s in stops:
            CreateStation(s,makegif=makegif)
    else:
        for s in stops:
            CreateStation_ENG(s,makegif=makegif)
    print(L+"素材制作完成")
#MakeLine(filename='station.txt',eng = False,makegif=False)

if __name__ == '__main__':
    print("V0.1 点阵模拟生成器  Author:BU5DR1V3R")
    print("本版本为初始版本，请注意：\n1.目前本系统没有任何错误信息预警、输入错误提示，请严格阅读Readme.txt文件后使用\n2.最后生成的文件会存放在infolib中，请自行查看")
    C1 = input("请输入录入文件的完整文件名，例如：station.txt 或：station-eng.txt\n")
    L = os.listdir()
    while C1 not in L:
        C1 = input("错误！未找到文件，请重新输入。")
        L = os.listdir()
    C2 = input("请问是否为英文站点，若是请输入1，若否请输入0：\n")
    if C2 == '1':
        eng = True
    else:
        eng = False
    C3 = input("请问是否需要生成动图？若是请输入1，若否请输入0：（注意，如果不生成动图，只会生成与字数长度相同的图片。）\n")
    if C3 == '1':
        makegif = True
    else:
        makegif = False
    C4 = input('是否使用BW格式？若是请输入1，若否请输入0（标点符号为英文，注意，线路号全角请在录入的txt文件中设置）\n')
    if C4 == '1':
        BW = True
    else:
        BW = False
    print("正在生成，请稍后。")
    MakeLine(filename=C1,eng = eng,makegif=makegif,BW=BW)
    print("生成完毕。")
