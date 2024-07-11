// Basic Javascript

function add() {
  const x = document.getElementById("num1").value;
  const y = document.getElementById("num2").value;

  document.getElementById("result").innerHTML = parseInt(x) + parseInt(y);
}

function reset() {
  document.getElementById("num1").value = "";
  document.getElementById("num2").value = "";
  document.getElementById("result").innerHTML = "";
}
