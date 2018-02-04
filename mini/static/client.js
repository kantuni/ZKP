/**
 * Created by Henrikh Kantuni on 12/13/17.
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
  let vote = document.getElementById('vote').value;
  let [a, b] = encrypt(pk, vote);
  let ballot = [credentials, a, b].join(',');

  let request = new Request('/ballot', {
    method: 'POST',
    body: ballot
  });

  fetch(request)
    .then(() => {
      ballots.push(ballot);
      board.insertAdjacentHTML('beforeend', `<li>${ballot}</li>`);
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
    .then(res => res.text())
    .then(m => {
      let yes = Number(m);
      let no = ballots.length - yes;
      console.log('Yes', yes);
      console.log('No', no);
    })
    .catch(error => {
      console.error(error);
    });
});
