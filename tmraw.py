#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import textwrap

def add_to_model(model, n, seq):
    seq = list(seq[:]) + [None]
    for i in range(len(seq)-n):
        gram = tuple(seq[i:i+n])
        next_item = seq[i+n]
        if gram not in model:
            model[gram] = []
        model[gram].append(next_item)

def markov_model(n, seq):
    model = {}
    add_to_model(model, n, seq)
    return model

def gen_from_model(n, model, start=None, max_gen=100):
    if start is None:
        start = random.choice(list(model.keys()))
    output = list(start)
    for i in range(max_gen):
        start = tuple(output[-n:])
        next_item = random.choice(model[start])
        if next_item is None:
            break
        else:
            output.append(next_item)
    return output

def markov_model_from_sequences(n, sequences):
    model = {}
    for item in sequences:
        add_to_model(model, n, item)
    return model

def markov_generate_from_sequences(n, sequences, count, max_gen=100):
    starts = [item[:n] for item in sequences if len(item) >= n]
    model = markov_model_from_sequences(n, sequences)
    return [gen_from_model(n, model, random.choice(starts), max_gen)
           for i in range(count)]

n=0
poema1 = ""
myline = ""

N_txt = 'cuervo.txt'
file = open(N_txt,"r").read().lower().splitlines()

while n<15:
    myline = random.choice(file)
    poema1 = poema1 + myline + "\n"
    n=n+1

print poema1

print "++++++"

words = poema1.split()
random.shuffle(words)

poema2= textwrap.fill(" ".join(words), 60)
print poema2

print "+++++++"

palabra="cuervo"
cambio="salchichón"
poema3 =  poema1.replace(palabra, cambio)

print poema3


print "++++++++++"

texto = [line.strip() for line in poema2.splitlines()]

for item in markov_generate_from_sequences(7, texto, 14):
    print "".join(item)


