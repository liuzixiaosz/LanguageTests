#!/usr/bin/env python3

import random

words_url = "./Words/Words.md"

file = open(words_url, "r+")
sentences = []

if __name__ == "__main__":
    sentences = file.readlines()
    random.shuffle(sentences)
    file.seek(0, 0)
    file.truncate()
    for each_line in sentences:
        if each_line != "\n":
            file.write(each_line + "\n")
    file.close()
