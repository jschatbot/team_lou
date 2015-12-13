# Usage
# python to_lou.py ./lou_dict/dic_dif.csv < input.txt
# input.txt must be tokenized

import sys

lines = sys.stdin.readlines()
lou_dict_file = open(sys.argv[1], 'r')

lou_dict = {}

for line in lou_dict_file:
    sp = line.rstrip('\n').split(',')
    lou_dict[sp[0]] = sp[4]

for line in lines:
    for word in line.split():
        if word in lou_dict:
            print lou_dict[word],
        else:
            print word,
    print
