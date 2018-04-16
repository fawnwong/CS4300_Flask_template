$(document).ready(function () {
  if(window.location.href.indexOf("search") > -1) {
    // window.location.href = (String(window.location.href) + "#results");
    $('html, body').animate({
      scrollTop: $('#output').offset().top
    }, {duration: 600, easing: 'swing'});
  }
});