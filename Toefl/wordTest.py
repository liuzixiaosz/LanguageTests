#!/usr/bin/env python3
import os, sys, requests, threading, random
from bs4 import BeautifulSoup

file_path = "./Words/Words.md"
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
        {   # 前景色
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        },

        'back' :
        {   # 背景
            'black'     : 40,  #  黑色
            'red'       : 41,  #  红色
            'green'     : 42,  #  绿色
            'yellow'    : 43,  #  黄色
            'blue'      : 44,  #  蓝色
            'purple'    : 45,  #  紫红色
            'cyan'      : 46,  #  青蓝色
            'white'     : 47,  #  白色
        },

        'mode' :
        {   # 显示模式
            'normal'    : 0,   #  终端默认设置
            'bold'      : 1,   #  高亮显示
            'underline' : 4,   #  使用下划线
            'blink'     : 5,   #  闪烁
            'invert'    : 7,   #  反白显示
            'hide'      : 8,   #  不可见
        },

        'default' :
        {
            'end' : 0,
        },
}


def usestyle(string, mode = '', fore = '', back = ''):
    #作者：JeanCheng
    #来源：CSDN
    #原文：https://blog.csdn.net/gatieme/article/details/45439671?utm_source=copy
    #版权声明：本文为博主原创文章，转载请附上博文链接！

    mode  = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'].keys() else ''

    fore  = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'].keys()else ''

    back  = '%s' % STYLE['back'][back] if back in STYLE['back'].keys() else ''

    style = ';'.join([s for s in [mode, fore, back] if s])

    style = '\033[%sm' % style if style else ''

    end   = '\033[%sm' % STYLE['default']['end'] if style else ''

    return '%s%s%s' % (style, string, end)

class MyBuff:
    def __init__(self, size):
        self.__size = size
        self.__que = []

    def flow(self, ele):
        if len(self.__que) == self.__size:
            self.__que.pop()
        self.__que.insert(0, ele)

    def get(self, idx):
        return self.__que[idx]

    def size(self):
        return len(self.__que)


def treatline(line):
    ita_words = []
    bold_words = []
    stack = []
    new_word = ""
    len_buff = 3
    buff = MyBuff(len_buff)
    rec_bold = False
    rec_ita = False
    for char in line:
        buff.flow(char)
        if char == "*":
            if (buff.size() == len_buff or buff.size() == len_buff - 1) and buff.get(len_buff - 2) == "*":
                if len(stack) > 0 and stack[len(stack) - 1] == "b":
                    stack = []
                    rec_bold = False
                    bold_words.append(new_word)
                    new_word = ""
                else:
                    stack.append("b")
                    rec_bold = True
            continue
        else:
            if (buff.size() == len_buff and buff.get(len_buff - 2) == "*" and buff.get(len_buff - 1) != "*" \
                    or (buff.size() == len_buff - 1 and buff.get(len_buff - 2) == "*")):
                if len(stack) > 0 and stack[len(stack) - 1] == "i":
                    stack = []
                    rec_ita = False
                    ita_words.append(new_word)
                    new_word = ""
                else:
                    stack.append("i")
                    rec_ita = True
        if rec_bold or rec_ita:
            new_word += char
    return bold_words, ita_words


def query(word):
    def get_item(ele_arr):
        for item in ele_arr:
            if item.text:
                print(usestyle(item.text, mode='bold', fore='green', back='black'))
        print(usestyle('-' * 40, mode='normal', fore='cyan', back='black'))

    try:
        r = requests.get(url=youdao_url % word)
        soup = BeautifulSoup(r.text, "lxml")
        s = soup.find(class_='trans-container')('ul')[0]('li')
        get_item(s)
        return
    except Exception:
        pass
    try:
        r = requests.get(url=bing_url % word)
        soup = BeautifulSoup(r.text, "lxml")
        s = soup.find(class_='qdef')('ul')[0]('li')
        get_item(s)
    except Exception:
        sys.stderr.write("Error occurs\n")

def test(sentences, all_len):
    global cnt
    rem = []
    for sen in sentences:
        cnt += 1
        print(usestyle("%d/%d" % (cnt, all_len), mode='normal', fore='green', back='black'))
        bolds, italics = treatline(sen)
        print(usestyle(sen, mode='bold', fore='white', back='black'))
        print(usestyle(str(bolds) + " " + str(italics), mode='bold', fore='yellow', back='black'))
        print("remembered?(y/Enter)")
        a = sys.stdin.readline()
        while a != "\n" and a != "y\n":
            a = sys.stdin.readline()
        for b in bolds:
            query(b)
            threading.Thread(target=lambda: os.system("say %s" % b)).start()
        print(usestyle('=' * 40, mode='normal', fore='cyan', back='black'))
        for i in italics:
            query(i)
            threading.Thread(target=lambda: os.system("say %s" % i)).start()
        print(usestyle('*' * 40 + '\n', mode='normal', fore='cyan', back='black'))
        if a == "y\n":
            rem.append(sen)
    return rem

def group_sentences(all_sentences):
    grouped = []
    clustered = []
    for sen in all_sentences:
        clustered.append(sen)
        if (len(clustered) == 10):
            grouped.append(clustered)
            clustered = []
    if (clustered != []):
        grouped.append(clustered)
    return grouped

def main():
    global cnt
    with open(file_path, "r") as f:
        all_sentences_raw = f.readlines()
        print("reading...")
        all_sentences = list(set(all_sentences_raw))
        all_sentences.remove('\n')
        print("Total sentences: %d" % len(all_sentences))
        shuf = input("shuffle? (y/other)")
        if shuf == 'y':
            random.shuffle(all_sentences)
        sentences_grp = group_sentences(all_sentences)
        for clu in sentences_grp:
            print(usestyle('new group starts', mode='normal', fore='red', back='black'))
            while len(clu) > 0:
                rem = test(clu, len(all_sentences))
                for r in rem:
                    clu.remove(r)
                cnt -= len(clu)

if __name__ == "__main__":
    main()


