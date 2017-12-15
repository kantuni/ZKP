""" Created by Henrikh Kantuni on 12/13/17 """

from random import randint

p = 283
q = 47
g = 60


def generate_keys():
    sk = randint(0, q - 1)
    pk = pow(g, sk, p)
    return pk, sk


def decrypt(sk, a, b):
    ai = pow(a, sk * (p - 2), p)
    gm = b * ai % p
    m = 0
    while pow(g, m, p) != gm:
        m += 1
    return m


def add(ciphers):
    a = 1
    b = 1
    for (ai, bi) in ciphers:
        a = (a * ai) % p
        b = (b * bi) % p
    return a, b
