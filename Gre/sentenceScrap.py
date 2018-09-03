#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys

url = "http://dict.youdao.com/w/%s/#keyfrom=dict2.top"
words_url = "./Words/Words.md"
words_raw_url = "./Words/WordsCopy.md"

f1 = open(file=words_url, mode="r+")
f2 = open(file=words_raw_url, mode="r+")
files = [f1, f2]

def get_index(txt, word):
    try:
        c = word[0]
        wd = c.upper() + word[1:]
        idx = txt.index(wd)
        return idx, wd
    except Exception:
        pass
    try:
        idx = txt.index(word + "s")
        return idx, word + "s"
    except Exception:
        pass
    try:
        idx = txt.index(word + "ed")
        return idx, word + "ed"
    except Exception:
        pass
    try:
        idx = txt.index(word)
        return idx, word
    except Exception:
        pass


def get_sentence(word):
    try:
        # 利用GET获取输入单词的网页信息
        r = requests.get(url=url % word)
        # 利用BeautifulSoup将获取到的文本解析成HTML
        soup = BeautifulSoup(r.text, "lxml")
        # 获取字典的标签内容
        s = soup.find(id='bilingual')('ul')[0]('li')
        # 输出字典的具体内容
        for item in s:
            if item.text:
                txt = str(item.text)
                try:
                    idx, pat = get_index(txt, word)
                    txt = txt.replace(pat, "**" + pat + "**")
                except Exception:
                    sys.stderr.write("not found the pattern\n")
                sys.stdout.write(txt)
                print("Write to files?(y)")
                if input() == "y":
                    txt = txt[1:]
                    new_line = txt[0: txt.index("\n") + 1]
                    for f in files:
                        f.write("\n" + new_line)
                    print("success")
                break
        print('-' * 40)
    except Exception:
        sys.stderr.write("Sorry, error happens\n")
        print('-' * 40)


if __name__ == '__main__':
    for f in files:
        f.seek(0, 2)
    while True:
        get_sentence(input())
        for f in files:
            f.flush()
