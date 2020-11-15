#!/usr/bin/env python
# coding=utf-8
# author: J.Wyss
# creation: 14.11.2020
# But: librarie des fonctions pour prendre un mot et le transformer en regex

import re
#create a dictionnary which takes as key a lowercase letter and contains as value a regex pattern which maches 0 to 2 times the letter
dict_alphabet = {}
dict_alphabet['a']='a{0,2}A{0,2}4{0,2}'
dict_alphabet['b']='b{0,2}B{0,2}'
dict_alphabet['c']='c{0,2}C{0,2}'
dict_alphabet['d']='d{0,2}D{0,2}'
dict_alphabet['e']='e{0,2}E{0,2}3{0,2}'
dict_alphabet['f']='f{0,2}F{0,2}'
dict_alphabet['g']='g{0,2}G{0,2}'
dict_alphabet['h']='h{0,2}H{0,2}'
dict_alphabet['i']='i{0,2}I{0,2}1{0,2}'
dict_alphabet['j']='j{0,2}J{0,2}'
dict_alphabet['k']='k{0,2}K{0,2}'
dict_alphabet['l']='l{0,2}L{0,2}'
dict_alphabet['m']='m{0,2}M{0,2}'
dict_alphabet['n']='n{0,2}N{0,2}'
dict_alphabet['o']='o{0,2}O{0,2}0{0,2}'
dict_alphabet['p']='p{0,2}P{0,2}'
dict_alphabet['q']='q{0,2}Q{0,2}'
dict_alphabet['r']='r{0,2}R{0,2}'
dict_alphabet['s']='s{0,2}S{0,2}5{0,2}'
dict_alphabet['t']='t{0,2}T{0,2}7{0,2}'
dict_alphabet['u']='u{0,2}U{0,2}'
dict_alphabet['v']='v{0,2}v{0,2}'
dict_alphabet['w']='w{0,2}W{0,2}'
dict_alphabet['x']='x{0,2}X{0,2}'
dict_alphabet['y']='y{0,2}Y{0,2}'
dict_alphabet['z']='z{0,2}Z{0,2}'
dict_alphabet[' ']='\s{0,2}'

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
