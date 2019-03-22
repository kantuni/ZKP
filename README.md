# ZKPs in Cryptographic Voting

Reference: [Cryptographic Voting – A Gentle Introduction](https://eprint.iacr.org/2016/765.pdf)

### Abstract

The main idea of this project is to present the notion of zero-knowledge proofs and their use in cryptographic voting. We will start with a primitive voting scheme called "mini-voting" that has few security issues. We will then create a new scheme (a variant of the "helios" scheme) based on the "mini-voting" that uses a concept of zero-knowledge proofs to solve these issues. We will see the implementation of two protocols that ensure zero-knowledge: Chaum-Pedersen and DCP (Disjunctive Chaum-Pedersen).

### Introduction

Let's start with a simple voting scheme called "mini-voting" for yes/no questions. The scheme consists of one "trusted" authority, a public bulletin board to which everyone (authority and voters) can post messages, and some number of voters. The encryption scheme used is the "Exponential ElGamal", which is a homomorphic assymetric encryption.

**Setup:** The authority creates a (public key, secret key) pair `(pk, sk)` using the scheme's key generation algorithm and posts the `pk` to the bulletin board. 

```python
def generate_keys():
    sk = randint(0, q - 1)
    pk = pow(g, sk, p)
    return pk, sk
```

**Voting:** Voters read the `pk` from the bulletin board. They can enter either 1 or 0 (yes / no), which will be encrypted (on the client side) using the scheme's encryption algorithm and will be posted on the board.

```js
function encrypt(pk, m) {
  let r = random(0, q - 1);
  let a = pow(g, r, p);
  let b = pow(g, m, p) * pow(pk, r, p) % p;
  return [a, b];
}
```

**Tallying:** The authority add all ballots using the scheme's add algorithm, decrypts the sum using the scheme's decryption algorithm, and outputs the result of the voting.

```python
def add(ciphers):
    a = 1
    b = 1
    for (ai, bi) in ciphers:
        a = (a * ai) % p
        b = (b * bi) % p
    return a, b
```

```python
def decrypt(sk, a, b):
    ai = pow(a, sk * (p - 2), p)
    gm = b * ai % p
    m = 0
    while pow(g, m, p) != gm:
        m += 1
    return m
```

### Security issues

"Mini-voting" is not secure, as participants can misbehave.

1. A voter can encrypt an invalid (not 0 or 1) vote, which will give him an unfair advantage.
2. The authority can decrypt incorrectly, i.e. announce a fake result.

There's also an issue with just having one "trusted" authority, which can be solved by using the threshold encryption scheme which uses n authorities instead of one. This way if at least one of the authorities is honest, the rest of them cannot misbehave. (threshold encryption is outside of the course of this project)

### Zero-Knowledge Proofs

Luckily, there is a solution to both of these issues – namely, zero-knowledge proofs.

> In cryptography, a **zero**-**knowledge** proof or **zero**-**knowledge** protocol is a method by which one party (the prover) can prove to another party (the verifier) that a given statement is true, without conveying any information apart from the fact that the statement is indeed true.

Each protocol will have a proof generation and a verification algorithm. A proof generation algorithm will produce a proof, so that anyone can check that the statement is indeed true using the verification algorithm.

#### Chaum-Pedersen's Protocol

To prove that the authority decrypted correctly we will use the following protocol.

```python
def correct_decryption_proof(pk, sk, a, b):
    r = randint(0, q - 1)
    u = pow(a, r, p)
    v = pow(g, r, p)
    c = custom_hash([pk, a, b, u, v])
    s = (r + (c * sk) % q) % q
    d = pow(a, sk, p)
    return u, v, s, d
```

```js
function checkDecryption(pk, cipher, proof) {
  let [a, b] = cipher;
  let [u, v, s, d] = proof;
  let c = customHash([pk, a, b, u, v]);
  return pow(a, s, p) === u * pow(d, c, p) % p && pow(g, s, p) === v * pow(pk, c, p) % p;
}
```

#### DCP (Disjunctive Chaum-Pedersen's) Protocol

Finally, to prove that a voter encrypted a valid vote (either 0 or 1) we will use the modification of Chaum-Pedersen's protocol - namely, DCP.

```js
function validVoteProof(pk, v, a, b, r) {
  let a0, a1, b0, b1, c0, c1, r0, r1;
  let c;

  if (v === 0) {
    c1 = random(0, q - 1);
    r0 = random(0, q - 1);
    r1 = random(0, q - 1);

    a1 = pow(g, r1, p) * pow(a, c1 * (p - 2), p) % p;
    b1 = pow(pk, r1, p) * pow(b * pow(g, p - 2, p) % p, c1 * (p - 2), p) % p;

    a0 = pow(g, r0, p);
    b0 = pow(pk, r0, p);

    c = customHash([pk, a, b, a0, b0, a1, b1]);
    // TODO: There is a problem with the notation in the paper.
    // c0 = Math.abs(c1 - c);
    c0 = (q + (c1 - c) % q) % q;

    r0 = (r0 + (c0 * r) % q) % q;
    return [a0, a1, b0, b1, c0, c1, r0, r1];
  } else if (v === 1) {
    c0 = random(0, q - 1);
    r0 = random(0, q - 1);
    r1 = random(0, q - 1);

    a0 = pow(g, r0, p) * pow(a, c0 * (p - 2), p) % p;
    b0 = pow(pk, r0, p) * pow(b, c0 * (p - 2), p) % p;

    a1 = pow(g, r1, p);
    b1 = pow(pk, r1, p);

    c = customHash([pk, a, b, a0, b0, a1, b1]);
    // TODO: There is a problem with the notation in the paper.
    // c1 = Math.abs(c0 - c);
    c1 = (q + (c0 - c) % q) % q;

    r1 = (r1 + (c1 * r) % q) % q;
    return [a0, a1, b0, b1, c0, c1, r0, r1];
  } else {
    // an adversary will tweak the code below
    return [0, 0, 0, 0, 0, 0, 0, 0];
  }
}
```

```python
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
```

This is it. I hope you have enjoyed it.  
Please feel free to open an issue or a pull request.
