var windowHeight = window.innerHeight;
var windowWidth = window.innerWidth;
console.log(windowHeight + " "+ windowWidth);

function clickFunc() {
  postPane.style.height = '33rem';
}

function closePane(){
  postPane.style.height = 0;

}

function clearFields() {
  document.getElementById("title").value = "";
  document.getElementById("message").value = "";
  document.getElementById("locTag").value = "";
  document.getElementById("tagTag").value = "";
}
