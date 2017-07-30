$(document).ready(function() {
//jQuery code goes here


function clickExpand() {
  /* Searches through multiple parents */
  var button = $(this);

  var cruxContent = button.parents(".buttonBar").next().children(".cruxContent").clone();
  var cruxTitle = button.parents(".buttonBar").next().children(".cruxTitle").clone();

  //Hacky JS for now, formatting can come later
  $(".cruxPopup").children(".popupText").html(cruxContent);
  $(".cruxPopup").children(".popupTitle").html(cruxTitle);

  $(".overlay").toggle();
  $(".cruxPopup").toggle();
}
/* Button selectors*/
$(".expandButton").click(clickExpand);



function clickTitlePopup1() {
  $(".overlay").toggle();
  $(".discussionSide1").toggle();
}
/* Button selectors*/
$(".discussion1PopupButton").click(clickTitlePopup1);



function clickTitlePopup2() {
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
