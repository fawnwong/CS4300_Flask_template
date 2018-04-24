$(document).ready(function () {
  if(window.location.href.indexOf("search") > -1) {
    // window.location.href = (String(window.location.href) + "#results");
    $('html, body').animate({
      scrollTop: $('#output').offset().top
    }, {duration: 600, easing: 'swing'});
  }
});

// function selectHandler() {
//   var selected = document.getElementById("search-select").value;
//   if (selected == "bot-com") {  
//     $(".by-bot-name").addClass("inactive");
//     $(".by-user-com").addClass("inactive");
//     $(".by-bot-com").removeClass("inactive");
//   } else if (selected == "user-com") {
//     $(".by-bot-name").addClass("inactive");
//     $(".by-user-com").removeClass("inactive");
//     $(".by-bot-com").addClass("inactive");
//   } else {
//     $(".by-bot-name").removeClass("inactive");
//     $(".by-user-com").addClass("inactive");
//     $(".by-bot-com").addClass("inactive"); 
//   }
// }

function learnHandler(element) {
  console.log("hi");
}