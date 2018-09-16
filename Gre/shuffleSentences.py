#!/usr/bin/env python3

import random

words_url = "./Words/Words.md"

f = open(words_url, "r+")
sentences = []

def main():
    sentences = f.readlines()
    random.shuffle(sentences)
    f.seek(0, 0)
    f.truncate()
    for each_line in sentences:
        if each_line != "\n":
            f.write(each_line + "\n")
    f.close()

if __name__ == "__main__":
    main()
