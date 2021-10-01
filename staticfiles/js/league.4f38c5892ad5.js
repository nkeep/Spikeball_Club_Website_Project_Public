// $(function(){
//   $('#lmatch').on('click', function() {
//     alert('hi');
//     var modal = $(this).children('#league-modal');
//     modal.css("display", "block");
//   });
// });

// $(function() {
//   $('.lmatch').click(function() {
//     $(this).children('.league-modal').fadeIn(300)
//   });'
// });

$(function() {
  var $standingson = $('#standings-on');
  var $standingsoff = $('#standings-off');
  var $toggleleague = $('#toggle-league');
  var $toggletournament = $('#toggle-tournament');
  $standingson.click(function() {
      $('.standings').toggle("slide", { direction: "right" }, 500);
      $(this).hide();
    });
  $standingsoff.click(function() {
    $('.standings').toggle("slide", { direction: "right" }, 500);
    $standingson.show();
  });


  $toggleleague.click(function() {
    $('.league-container').toggle("slide", {direction:"up"}, 1000);
  });

  $toggletournament.click(function() {
    $(this).css("background-color", "black");
    $(this).css("color", "white");
    $('.ltournament-container').toggle("slide", {direction:"up"}, 1000);
  });
});
