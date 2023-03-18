$(document).ready(function () {
  $("body").on('click', '.custom-modal .cancel', function () {
    $(".modal").removeClass("is-active");
    console.log('Stänger modal');
  });
});


setTimeout(function() {
  document.querySelectorAll('.alert').forEach(function(el) {
    el.classList.add('hide');
    el.remove();
  });
}, 4000);


// Lägg till en klickhändelse på varje rad i tabellen med spelare
var rows = document.getElementsByTagName("tr");
for (var i = 0; i < rows.length; i++) {
  rows[i].style.cursor = "pointer";
  rows[i].onclick = function() {
    window.location = this.getAttribute("data-href");
  };
}