/**
 * Created by Henrikh Kantuni on 12/14/17.
 */


function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function pow(x, y, z) {
  let ans = 1;
  while (y > 0) {
    if (y % 2 === 1) {
      ans = (ans * x) % z;
    }
    x = (x * x) % z;
    y = Math.floor(y / 2);
  }
  return ans;
}

function encrypt(pk, m) {
  let r = random(0, q - 1);
  let a = pow(g, r, p);
  let b = pow(g, m, p) * pow(pk, r, p) % p;
  return [a, b];
}
