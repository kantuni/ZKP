""" Created by Henrikh Kantuni on 12/13/17 """

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
    with open('ballots.csv', 'a') as file:
        file.write(data + '\n')
    return '', 200


@app.route('/tally', methods=['POST'])
def tally():
    ballots = []
    with open('ballots.csv', 'r') as file:
        for line in file:
            _, a, b = line.strip().split(',')
            ballots.append((int(a), int(b)))

    a, b = crypto.add(ballots)
    total = crypto.decrypt(sk, a, b)
    return str(total)


if __name__ == '__main__':
    pk, sk = crypto.generate_keys()
    if os.path.isfile('ballots.csv'):
        os.remove('ballots.csv')

    app.run()
