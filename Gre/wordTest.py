#!/usr/bin/env python3
# -- coding :utf-8 --
import os, sys, requests, threading, random
from bs4 import BeautifulSoup
from mydict import *

file_path = "./Words/Words.md"


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
    lookup(word, get_item, 0)


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
        else:
            all_sentences.sort()
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
