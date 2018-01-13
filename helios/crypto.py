""" Created by Henrikh Kantuni on 12/14/17 """

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


def custom_hash(values):
    h = 0
    for i in range(len(values)):
        h = (h + pow(10, i) * values[i] % q) % q
    return h


def correct_decryption_proof(pk, sk, a, b):
    r = randint(0, q - 1)
    u = pow(a, r, p)
    v = pow(g, r, p)
    c = custom_hash([pk, a, b, u, v])
    s = (r + (c * sk) % q) % q
    d = pow(a, sk, p)
    return u, v, s, d


def verify_vote(pk, cipher, proof):
    a, b = cipher
    a0, a1, b0, b1, c0, c1, r0, r1 = proof

    s1 = pow(g, r0, p) == a0 * pow(a, c0, p) % p
    s2 = pow(g, r1, p) == a1 * pow(a, c1, p) % p
    s3 = pow(pk, r0, p) == b0 * pow(b, c0, p) % p
    s4 = pow(pk, r1, p) == b1 * pow(b * pow(g, p - 2, p) % p, c1, p) % p
    # TODO: There is a problem with the notation in the paper.
    # s5 = (c0 + c1) % q == custom_hash([pk, a, b, a0, b0, a1, b1])
    return s1 and s2 and s3 and s4
