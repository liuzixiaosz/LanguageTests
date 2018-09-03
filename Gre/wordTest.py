#!/usr/bin/env python3
import os, sys, requests, threading, random
from bs4 import BeautifulSoup

file_path = "./Words/Words.md"
youdao_url = "http://dict.youdao.com/w/%s/#keyfrom=dict2.top"
bing_url = "http://cn.bing.com/dict/search?q=%s"
cluster = 5
cnt = 0

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
                print(item.text)
        print('-' * 40)

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
        print("%d/%d" % (cnt, all_len))
        bolds, italics = treatline(sen)
        print(sen)
        print(str(bolds) + " " + str(italics))
        print("remembered?(y/Enter)")
        a = sys.stdin.readline()
        while a != "\n" and a != "y\n":
            a = sys.stdin.readline()
        for b in bolds:
            query(b)
            threading.Thread(target=lambda: os.system("say %s" % b)).start()
        print('=' * 40)
        for i in italics:
            query(i)
            threading.Thread(target=lambda: os.system("say %s" % i)).start()
        print("*" * 40 + "\n")
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

if __name__ == "__main__":

    with open(file_path, "r") as f:
        all_sentences_raw = f.readlines()
        print("reading...")
        all_sentences = list(set(all_sentences_raw))
        all_sentences.remove('\n')
        if input("shuffle?(y/other)") == "y":
            random.shuffle(all_sentences)
        print("Total sentences: %d" % len(all_sentences))
        sentences_grp = group_sentences(all_sentences)
        for clu in sentences_grp:
            print("new group starts!")
            while len(clu) > 0:
                rem = test(clu, len(all_sentences))
                for r in rem:
                    clu.remove(r)
                cnt -= len(clu)

        
