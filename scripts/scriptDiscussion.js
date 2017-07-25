$(document).ready(function() {
//jQuery code goes here

function clickExpand() {
  var button = $(this);

  var crux = $(this).parents(".text").children(".cruxContent").html();

  //Hacky JS for now, formatting can come later
  $(".introPopup").append(crux);

  $(".overlay").toggle();
  $(".introPopup").toggle();
}

$(".expandButton").click(clickExpand);

});
