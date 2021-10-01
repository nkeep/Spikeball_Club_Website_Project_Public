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

  var $teamson = $('#teams-on');
  var $teamsoff = $('#teams-off');
  var $posteron = $('#poster-on');
  var $posteroff = $('#poster-off');

  $posteron.click(function(){
    $('.tournament-poster').toggle("slide", {direction:"right"}, 500);
    $('.signup-buttons').hide()
  });

  $posteroff.click(function(){
    $('.tournament-poster').toggle("slide", {direction:"right"}, 500);
    $('.signup-buttons').show()
  });

  $teamson.click(function(){
    $('.signed-up-teams').toggle("slide", {direction:"right"}, 500);
    $('.signup-buttons').hide()
  });

  $teamsoff.click(function(){
    $('.signed-up-teams').toggle("slide", {direction:"right"}, 500);
    $('.signup-buttons').show()
  });


});
