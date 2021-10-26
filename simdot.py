import binascii,copy
import numpy as np
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片

SAVEPATH = ".\\output\\"
OFFSET = 23
FONTLIB = "HZK16"#HZK16需要转置后使用
L = ['，','。','（','）','、','“','”']
N = ['１','２','３','４','５','６','７','８','９','０']
#以下三个函数只跟16*16的字点阵有关
def IS_CHINESE(ch):
    if '\u4e00' <= ch <= '\u9fff' or ch in L or ch in N:
        return True
    return False
    
def CHA2HZK16(word): 
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示，需要32个字节才能显示一个汉字
    # 之所以32字节：256个点每个点是0或1，那么总共就是2的256次方，一个字节是2的8次方
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)
    text = word
    if not IS_CHINESE(word):
        return np.zeros((16,16),dtype = int)
    #获取中文的gb2312编码，一个汉字是由2个字节编码组成
    gb2312 = text.encode('gb2312')
    #将二进制编码数据转化为十六进制数据
    hex_str = binascii.b2a_hex(gb2312)
    #将数据按unicode转化为字符串
    result = str(hex_str, encoding='utf-8')
    #前两位对应汉字的第一个字节：区码，每一区记录94个字符
    area = eval('0x' + result[:2]) - 0xA0
    #后两位对应汉字的第二个字节：位码，是汉字在其区的位置
    index = eval('0x' + result[2:]) - 0xA0
    #汉字在HZK16中的绝对偏移位置，最后乘32是因为字库中的每个汉字字模都需要32字节
    offset = (94 * (area-1) + (index-1)) * 32
    font_rect = None
    #读取HZK16汉字库文件 
    with open(".\\font_libs\\HZK\\16\\"+FONTLIB, "rb") as f:
        #找到目标汉字的偏移位置
        f.seek(offset)
        #从该字模数据中读取32字节数据
        font_rect = f.read(32)
    #print(font_rect)
    #font_rect的长度是32，此处相当于for k in range(16)
    for k in range(len(font_rect) // 2):
        #每行数据
        row_list = rect_list[k]
        for j in range(2):
            for i in range(8):
                asc = font_rect[k * 2 + j]
                #此处&为Python中的按位与运算符
                flag = asc & KEYS[i]
                #数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                row_list.append(flag)
    if FONTLIB == 'HZK16':
        rect_list = np.array(rect_list).T
    #print(rect_list)
    #根据获取到的16*16点阵信息，打印到控制台
    res = copy.deepcopy(rect_list)
    for i in range(16):
        for j in range(16):
            if res[i][j]!=0:
                res[i][j]='1'
            #print(res[i][j],end=" ")
        #print()
    return res

def LETTER216(lt):
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)
    offset = ord(lt)
    with open(".\\font_libs\\ASC\\ASC16_8", "rb") as f:
        f.seek((offset-32)*16)
        font_rect = f.read(16)
    for i in range(16):
        row_list = rect_list[i]
        for j in range(8):
            index = j*16+i
            flag = font_rect[index//8] & KEYS[index%8]
            row_list.append(flag)
    #print(np.array(rect_list))
    for i in range(16):
        for j in range(8):
            if rect_list[i][j]>0:
                rect_list[i][j]=1
    return np.array(rect_list)

def CirclePixel(COLOR = [224,0,0]): #用21*21模拟一个圆形像素点，外面加一圈到23*23
    #OFFSET = 23
    #CIRCLE21 = [23,7,5,4,3,2,1,1,0,0,0]
    CIRCLE21 = [23,8,6,5,4,3,2,2,1,1,1]
    C21 = copy.deepcopy(CIRCLE21)
    CIRCLE21.reverse()
    C21_R = copy.deepcopy(CIRCLE21)
    C = C21+[1]+C21_R
    res = np.zeros((OFFSET,OFFSET,3),dtype='uint8')
    for i in range(OFFSET):
        for j in range(OFFSET):
            if j>=C[i] and j<=OFFSET-C[i]-1:
                res[i][j] = COLOR
    #plt.imsave('Circle.png', res)
    return res
          
def DrawCharacter(ch):
    src = CHA2HZK16(ch)
    #OFFSET = 23
    output = np.zeros((16*OFFSET,16*OFFSET,3),dtype='uint8')
    RED = CirclePixel(COLOR = [224,0,0])
    BLACK = CirclePixel(COLOR = [40,40,40])
    for i in range(0,16):
        for j in range(0,16):
            if src[i][j] == 0:
                for k in range(i*OFFSET,i*OFFSET+OFFSET):
                    for l in range(j*OFFSET,j*OFFSET+OFFSET):
                        output[k][l] = BLACK[k%OFFSET][l%OFFSET]
            else:
                for k in range(i*OFFSET,i*OFFSET+OFFSET):
                    for l in range(j*OFFSET,j*OFFSET+OFFSET):
                        output[k][l] = RED[k%OFFSET][l%OFFSET]
    #plt.imsave(SAVEPATH+ch+'.png', output)
    return output

def DrawLetter(lt):
    src = LETTER216(lt)
    #OFFSET = 23
    output = np.zeros((16*OFFSET,8*OFFSET,3),dtype='uint8')
    RED = CirclePixel(COLOR = [224,0,0])
    BLACK = CirclePixel(COLOR = [40,40,40])
    for i in range(0,16):
        for j in range(0,8):
            if src[i][j] == 0:
                for k in range(i*OFFSET,i*OFFSET+OFFSET):
                    for l in range(j*OFFSET,j*OFFSET+OFFSET):
                        output[k][l] = BLACK[k%OFFSET][l%OFFSET]
            else:
                for k in range(i*OFFSET,i*OFFSET+OFFSET):
                    for l in range(j*OFFSET,j*OFFSET+OFFSET):
                        output[k][l] = RED[k%OFFSET][l%OFFSET]
    #plt.imsave(SAVEPATH+ch+'.png', output)
    return output

def DrawSentence(sentence,outname = 'Test',savepath = SAVEPATH,save=True):#句子
    #OFFSET = 23
    #设计：这里就头顶头做点阵即可
    res = np.zeros((16*OFFSET,len(sentence)*16*OFFSET,3),dtype='uint8')
    nowwidth = 0
    for idx in range(len(sentence)):
        print("Drawing Char No. %d"%idx)
        if IS_CHINESE(sentence[idx]):
            pic = DrawCharacter(sentence[idx])
            width = 16
        else:
            pic = DrawLetter(sentence[idx])
            width = 8
        for i in range(OFFSET*16):
            for j in range(nowwidth,nowwidth+width*OFFSET):
                if nowwidth!=0:
                    res[i][j] = pic[i][j%nowwidth]
                else:
                    res[i][j] = pic[i][j]
        nowwidth+=width*OFFSET
    output = np.zeros((16*OFFSET,nowwidth,3),dtype='uint8')
    for i in range(16*OFFSET):
        for j in range(nowwidth):
            output[i][j] = res[i][j]
    if save:
        plt.imsave(savepath+outname+'.png', output)
        print('DONE')
    else:
        print('DONE')
    return output