#!/usr/bin/env python
# coding=utf-8
# author: J.Wyss
# creation: 14.11.2020
# But: librarie des fonctions pour prendre un mot et le transformer en regex

import re
#create a dictionnary which takes as key a lowercase letter and contains as value a regex pattern which maches 0 to 2 times the letter
dict_alphabet = {}
dict_alphabet['a']='a+|A+|4+'
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
dict_alphabet['.']='\s*'

#dict_alphabet = {}
#dict_alphabet['a']='[aA4]'
#dict_alphabet['b']='[bB]'
#dict_alphabet['c']='[cC]'
#dict_alphabet['d']='[dD]'
#dict_alphabet['e']='[eE3]'
#dict_alphabet['f']='[fF]'
#dict_alphabet['g']='[gG]'
#dict_alphabet['h']='[hH]'
#dict_alphabet['i']='[iI]'
#dict_alphabet['j']='[jJ]'
#dict_alphabet['k']='[kK]'
#dict_alphabet['l']='[lL]'
#dict_alphabet['m']='[mM]'
#dict_alphabet['n']='[nN]'
#dict_alphabet['o']='[oO0'
#dict_alphabet['p']='[pP]'
#dict_alphabet['q']='[qQ]'
#dict_alphabet['r']='[rR]'
#dict_alphabet['s']='[sS5]'
#dict_alphabet['t']='[tT7]'
#dict_alphabet['u']='[uU]'
#dict_alphabet['v']='[vV]'
#dict_alphabet['w']='[wW]'
#dict_alphabet['x']='[xX]'
#dict_alphabet['y']='[yY]'
#dict_alphabet['z']='[zZ]'
#dict_alphabet[' ']='\s'
#dict_alphabet['.']='\s'
def word_to_regex(word: str):
    l = []
    seperator=''
    for i in range(0, len(word)):
        try:
            l.append('('+dict_alphabet[word[i].lower()]+'){1}')
        except:
            l.append("\w")
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
    print(re.search(res, test_1))
    #for i in list_of_birds_test:
