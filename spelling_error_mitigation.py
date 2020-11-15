#!/usr/bin/env python
# coding=utf-8
# author: J.Wyss
# creation: 14.11.2020
# But: librarie des fonctions pour prendre un mot et le transformer en regex

import re
#create a dictionnary which takes as key a lowercase letter and contains as value a regex pattern which maches 0 to 2 times the letter
dict_alphabet = {}
dict_alphabet['a']='a+|A+|4{1,3}'
dict_alphabet['b']='b+|B+'
dict_alphabet['c']='c+|C+'
dict_alphabet['d']='d+|D+'
dict_alphabet['e']='e+|E+|3+'
dict_alphabet['f']='f+|F+'
dict_alphabet['g']='g+|G+'
dict_alphabet['h']='h+|H+'
dict_alphabet['i']='i+|I+|1+'
dict_alphabet['j']='j+|J+'
dict_alphabet['k']='k+|K+'
dict_alphabet['l']='l+|L+'
dict_alphabet['m']='m+|M+'
dict_alphabet['n']='n+|N+'
dict_alphabet['o']='o+|O+|0+'
dict_alphabet['p']='p+|P+'
dict_alphabet['q']='q+|Q+'
dict_alphabet['r']='r+|R+'
dict_alphabet['s']='s+|S+|5+'
dict_alphabet['t']='t+|T+|7+'
dict_alphabet['u']='u+|U+'
dict_alphabet['v']='v+|V+'
dict_alphabet['w']='w+|W+'
dict_alphabet['x']='x+|X+'
dict_alphabet['y']='y+|Y+'
dict_alphabet['z']='z+|Z+'
dict_alphabet[' ']='\s+'

def word_to_regex(word: str):
    l = []
    seperator=''
    for i in range(0, len(word)):
       l.append("("+dict_alphabet[word[i].lower()]+"){1}")
    res= seperator.join(l)
    return res


if __name__ == '__main__':
    test_1 = 'hdegegfgfe pakrrot gezdlzted african grey'
    test = 'african grey'
    res = word_to_regex(test)
    list_of_birds_test = ["bird", "ara", "amazon", "amazona", "parrot", "african grey", "macaw", "cockatoo"]

    for i in list_of_birds_test:
        print(word_to_regex(i))
    print(res, type(res))
    #for i in list_of_birds_test:
