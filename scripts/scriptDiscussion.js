$(document).ready(function() {
//jQuery code goes here

var toggleCheck = true;

function clickExpand() {
  var button = $(this);

  /* Searches through multiple parents */
  var crux = $(this).parents(".text").children(".cruxContent").html();

  //Hacky JS for now, formatting can come later
  $(".cruxPopup").children(".popupText").html(crux);

  $(".overlay").toggle();
  $(".cruxPopup").toggle();
}

function clickExpand2() {
  var button = $(this);

  /* Searches through multiple parents */
  var crux = $(this).parents(".text").children(".cruxContent").html();

  /* How far you've scrolled */
  var topVal = $(window).scrollTop();

  //Hacky JS for now, formatting can come later
  $(".cruxPopup").children(".popupText").html(crux);

  /* Attempts to get popup to show up centered on page, but not yet working */
  $(".cruxPopup").css({top : topVal});

  $(".overlay").toggle();
  $(".cruxPopup").toggle();
}

/* Button selectors*/
$(".expandButton").click(clickExpand2);
$(".closeExpandButton").click(clickExpand);


function onHold() {
  var button = $(this);

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/onhold', {"crux_key": urlsafeKey}, function(response) {
  });

  $(this).parent().parent().toggleClass("onHold");
}

$(".onHoldButton").click(onHold);


function onAccept() {
  var button = $(this);

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/onaccept', {"crux_key": urlsafeKey}, function(response) {
  });

  $(this).parent().parent().toggleClass("onAccept");
}

$(".onAcceptButton").click(onAccept);

});
