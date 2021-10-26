import imageio
from PIL import Image
import pandas as pd
import numpy as np

def img2gif(image, offset=23, from_='r', scroll_size=23*12*16, has_out=True, bgc=''):
    """
    offset: 每次移动像素
    from: l, r, u, d  对应左右上下
    scroll_size: 滚动窗口大小
    has_out: 是否滚出窗口
    bgc: 填充颜色
    """
    # 反转坐标标记 [::1]正常  [::-1]反转
    rev_flag = 1 if from_ in 'lr' else -1    
    # 图片在移动方向和静止方向的尺寸
    move_axis, static_axis = image.size[::rev_flag]
    # 滚动窗口的尺寸（仅移动方向，静止方向与图片一样）
    scroll_size = scroll_size if scroll_size else move_axis  
    # 滚出窗口的补充
    scoll_out = scroll_size if has_out else 0
    # 左->右  上->下
    if from_ in 'lu':
        range_ = range(-move_axis, scoll_out, offset)
    # 右->左  下->上
    elif from_ in 'rd':        
        range_ = range(scroll_size, scroll_size - move_axis - scoll_out, -offset)
    image_ls = []
    for i in range_:
        #new_img = Image.new(mode="RGBA", size=[scroll_size, static_axis][::rev_flag], color=bgc)
        new_img =Image.open('.\\pic\\bkgrnd.png')
        new_img.paste(image, (i, 0)[::rev_flag])
        image_ls.append(new_img)
    return image_ls

# 读取图片
#image = Image.open('.\\output\\沪南路北中路（北蔡） 到了.png')
#print(np.array(image))
#out = img2gif(image, offset=46, from_='r', has_out=True)
#imageio.mimsave('.\\output\\out.gif', out , 'GIF', duration=0.05)