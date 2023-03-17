$(document).ready(function () {
  $("div#matchModal").on('click', '.cancel', function () {
    $(".modal").removeClass("is-active");
    console.log('Stänger modal');
  });
});

setTimeout(function() {
  document.querySelectorAll('.alert').forEach(function(el) {
    el.classList.add('hide');
  });
}, 3000);