$(document).ready(function() {
//jQuery code goes here

var toggleCheck = true;

function clickExpand() {
  var button = $(this);

  var crux = $(this).parents(".text").children(".cruxContent").html();

  //Hacky JS for now, formatting can come later
  $(".cruxPopup").children(".popupText").html(crux);

  $(".overlay").toggle();
  $(".cruxPopup").toggle();
}

$(".expandButton").click(clickExpand);


function clickButton() {

  // Here, "this" is the button that the user clicked.
  var button = $(this);

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/onhold', {"crux_key": urlsafeKey}, function(response) {
  });

  $(this).parent().toggleClass("onHold");
}

$(".onHoldButton").click(clickButton);


});
