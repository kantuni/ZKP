/**
 * Created by Henrikh Kantuni on 12/14/17.
 */


let g, p, q, pk;
let board, ballots;


window.onload = () => {
  board = document.getElementById('board');
  let request = new Request('/setup', {
    method: 'POST'
  });

  fetch(request)
    .then(res => res.json())
    .then(data => {
      ({p, q, g, pk, ballots} = data);
      board.insertAdjacentHTML('beforeend', `<li>Public Key = ${pk}</li>`);
      ballots.map(ballot => board.insertAdjacentHTML('beforeend', `<li>${ballot}</li>`));
    })
    .catch(error => {
      console.error(error);
    });
};

document.getElementById('send').addEventListener('click', e => {
  e.preventDefault();

  let credentials = document.getElementById('credentials').value;
  let vote = parseInt(document.getElementById('vote').value, 10);
  let [a, b, proof] = encrypt(pk, vote);
  let cipher = [a, b];

  let request = new Request('/ballot', {
    method: 'POST',
    body: JSON.stringify({credentials, cipher, proof})
  });

  fetch(request)
    .then(res => res.text())
    .then(res => {
      if (res === 'Access') {
        let ballot = [credentials, a, b, proof].join(',');
        ballots.push(ballot);
        board.insertAdjacentHTML('beforeend', `<li>${ballot}</li>`);
      } else {
        alert("The vote is not valid");
      }
    })
    .catch(error => {
      console.error(error);
    });
});

document.getElementById('tally').addEventListener('click', e => {
  e.preventDefault();

  let request = new Request('/tally', {
    method: 'POST'
  });

  fetch(request)
    .then(res => res.json())
    .then(data => {
      console.log(data);
      let {cipher, proof} = data;
      if (!verifyDecryption(pk, cipher, proof)) {
        alert("The decryption proof is not valid.");
      }
    })
    .catch(error => {
      console.error(error);
    });
});
