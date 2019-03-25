#!/usr/bin/env python3
# -- coding :utf-8 --

import os, sys, requests, threading, random
from bs4 import BeautifulSoup

youdao_url = "http://dict.youdao.com/w/%s/#keyfrom=dict2.top"
bing_url = "http://cn.bing.com/dict/search?q=%s"
cluster = 5
cnt = 0

#   格式：\033[显示方式;前景色;背景色m
#   说明:
#
#   前景色            背景色            颜色
#   ---------------------------------------
#     30                40              黑色
#     31                41              红色
#     32                42              绿色
#     33                43              黃色
#     34                44              蓝色
#     35                45              紫红色
#     36                46              青蓝色
#     37                47              白色
#
#   显示方式           意义
#   -------------------------
#      0           终端默认设置
#      1             高亮显示
#      4            使用下划线
#      5              闪烁
#      7             反白显示
#      8              不可见
#
#   例子：
#   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
#   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]


STYLE = {
    'fore':
        {  # 前景色
            'black': 30,  # 黑色
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple': 35,  # 紫红色
            'cyan': 36,  # 青蓝色
            'white': 37,  # 白色
        },

    'back':
        {  # 背景
            'black': 40,  # 黑色
            'red': 41,  # 红色
            'green': 42,  # 绿色
            'yellow': 43,  # 黄色
            'blue': 44,  # 蓝色
            'purple': 45,  # 紫红色
            'cyan': 46,  # 青蓝色
            'white': 47,  # 白色
        },

    'mode':
        {  # 显示模式
            'normal': 0,  # 终端默认设置
            'bold': 1,  # 高亮显示
            'underline': 4,  # 使用下划线
            'blink': 5,  # 闪烁
            'invert': 7,  # 反白显示
            'hide': 8,  # 不可见
        },

    'default':
        {
            'end': 0,
        },
}

def usestyle(string, mode='', fore='', back=''):
    # 作者：JeanCheng
    # 来源：CSDN
    # 原文：https://blog.csdn.net/gatieme/article/details/45439671?utm_source=copy
    # 版权声明：本文为博主原创文章，转载请附上博文链接！

    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'].keys() else ''

    fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'].keys() else ''

    back = '%s' % STYLE['back'][back] if back in STYLE['back'].keys() else ''

    style = ';'.join([s for s in [mode, fore, back] if s])

    style = '\033[%sm' % style if style else ''

    end = '\033[%sm' % STYLE['default']['end'] if style else ''

    return '%s%s%s' % (style, string, end)

def lookup(word, get_item, *idx):
    def fetch_idx(dictname):
        if dictname == 'yd':
            for this_idx in idx:
                if this_idx == 0:
                    s = soup.find(class_='trans-container')('ul')[0]('li')
   #             elif this_idx == 1:
  #                  s = soup.find(id='synonyms')
#                elif this_idx == 2:
 #                   s = soup.find(id='bilingual')('ul')[0]('li')
                get_item(s)
        elif dictname == 'bing':
            for this_idx in idx:
                if this_idx == 0:
                    s = soup.find(class_='qdef')('ul')[0]('li')
#                elif this_idx == 1:
#                    s = soup.find(id='df_div2')
#                elif this_idx == 2:
#                    s = soup.find(id='sentenceSeg')
                get_item(s)
    try:
        r = requests.get(url=youdao_url % word)
        soup = BeautifulSoup(r.text, "lxml")
        fetch_idx('yd')
        return
    except Exception:
        pass
    try:
        r = requests.get(url=bing_url % word)
        soup = BeautifulSoup(r.text, "lxml")
        fetch_idx('bing')
    except Exception:
        sys.stderr.write("Error occurs\n")

def default_get_item(ele_arr):
    for item in ele_arr:
        print(usestyle(str(item.text).strip(), mode='bold', fore='green', back='black'))

def main():
    while 1:
        #lookup(input(), default_get_item, 0, 1, 2)
        lookup(input(), default_get_item, 0)

if __name__ == '__main__':
    main()

