""" Created by Henrikh Kantuni on 12/14/17 """

from flask import Flask, request, render_template
import crypto
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/setup', methods=['POST'])
def setup():
    ballots = []
    with open('ballots.csv', 'a+') as file:
        file.seek(0)
        for line in file:
            ballots.append(line.strip())

    response = {
        'p': crypto.p,
        'q': crypto.q,
        'g': crypto.g,
        'pk': pk,
        'ballots': ballots
    }
    return json.dumps(response)


@app.route('/ballot', methods=['POST'])
def ballot():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    credentials = data['credentials']
    cipher = data['cipher']
    proof = data['proof']

    if crypto.verify_vote(pk, cipher, proof):
        with open('ballots.csv', 'a') as file:
            cipher = [str(s) for s in cipher]
            proof = [str(s) for s in proof]
            line = '{0},{1},{2}\n'.format(credentials, ','.join(cipher), ','.join(proof))
            file.write(line)
        return 'Access', 200
    return 'Denied', 200


@app.route('/tally', methods=['POST'])
def tally():
    ballots = []
    with open('ballots.csv', 'r') as file:
        for line in file:
            line = line.strip().split(',')
            ballots.append((int(line[1]), int(line[2])))

    a, b = crypto.add(ballots)
    yes = crypto.decrypt(sk, a, b)
    proof = crypto.correct_decryption_proof(pk, sk, a, b)
    response = {
        'yes': yes,
        'no': len(ballots) - yes,
        'cipher': [a, b],
        'proof': proof
    }
    return json.dumps(response)


if __name__ == '__main__':
    pk, sk = crypto.generate_keys()
    if os.path.isfile('ballots.csv'):
        os.remove('ballots.csv')

    app.run()
