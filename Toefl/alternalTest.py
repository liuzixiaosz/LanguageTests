#!/usr/bin/env python3
import os, sys, random

alt_url = "./Words/AlternativeWords.txt"
file = open(alt_url, "r")
dict = {}


def read_all():
    line = file.readline()
    while len(line) > 0:
        sepered = line.split(":")
        try:
            all_alt = sepered[1].strip().split(",")
        except IndexError:
            all_alt = sepered[1].strip()
        dict[sepered[0]] = all_alt
        line = file.readline()


if __name__ == '__main__':
    read_all()
    items_arr = []
    for k, v in dict.items():
        items_arr.append(k)

    for k in items_arr:
        print(k)
        alt_arr = dict.get(k)
        word = ""
        cnt = 0
        input_before = []
        while word != "#":
            word = input()
            if word in alt_arr:
                if word not in input_before:
                    input_before.append(word)
                    cnt += 1
                    print("√")
                else:
                    print("you input it before")
            else:
                print("X")
            if cnt == len(alt_arr):
                word = "#"
            print("%s/%s" % (cnt, len(alt_arr)))
        print("-")
