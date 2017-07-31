$(document).ready(function() {
//jQuery code goes here


function clickExpand() {
  /* Searches through multiple parents */
  var button = $(this);

  var cruxTitle = button.children(".cruxTitle").text();
  var cruxContent = button.children(".cruxContent").text();

  //Hacky JS for now, formatting can come later
  $(".cruxPopup").children(".popupTitle").text(cruxTitle);
  $(".cruxPopup").children(".popupText").text(cruxContent);

  $(".popupTitle").css("font-weight","Bold");

  $(".overlay").toggle();
  $(".cruxPopup").toggle();
}
/* Button selectors*/
$(".expandButton").click(clickExpand);


// Test out these updated buttons to see if the text from the title will show.


function clickTitlePopup1() {
  title = $("#side1Title").text();

  $("#title1Popup").text(title);

  $(".overlay").toggle();
  $(".discussionSide1").toggle();
}
/* Button selectors*/
$(".discussion1PopupButton").click(clickTitlePopup1);



function clickTitlePopup2() {
  title = $("#side2Title").text();

  $("#title2Popup").text(title);

  $(".overlay").toggle();
  $(".discussionSide2").toggle();
}
/* Button selectors*/
$(".discussion2PopupButton").click(clickTitlePopup2);



// function onHold() {
//   var button = $(this);
//
//   // Get the URLsafe key from the button value.
//   var urlsafeKey = $(button).val();
//
//   // Send a POST request and handle the response.
//   $.post('/onhold', {"crux_key": urlsafeKey}, function(response) {
//   });
//
//   $(this).parent().parent().toggleClass("onHold");
// }
// $(".onHoldButton").click(onHold);
//
//
//
//
// function onAccept() {
//   var button = $(this);
//
//   // Get the URLsafe key from the button value.
//   var urlsafeKey = $(button).val();
//
//   // Send a POST request and handle the response.
//   $.post('/onaccept', {"crux_key": urlsafeKey}, function(response) {
//   });
//
//   $(this).parent().toggleClass("onAccept");
// }
// $(".onAcceptButton").click(onAccept);


function showMenu() {
  var menu = $(this);
  menu.toggleClass("change");
  menu.parent().children(".hidden").toggle();
  menu.parent().children(".helpertext").toggle();
}
$(".menu_container").click(showMenu)



});
