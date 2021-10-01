$(function() {
  // standings table
  var $standingson = $('#standings-on');
  var $standingsoff = $('#standings-off');

  $standingson.click(function() {
      $('.standings').toggle("slide", { direction: "right" }, 500);
      $(this).hide();
    });
  $standingsoff.click(function() {
    $('.standings').toggle("slide", { direction: "right" }, 500);
    $standingson.show();
  });

  // Signup page
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

  //League functionality

  //Tournament Functionality
  $('.toggle-container').click(function(){
    $(this).next().toggle("slide", {direction:"up"}, 500);
    if ($(this).is('.off')){
      $(this).removeClass('off');
      $(this).addClass('on');
    }
    else{
      $(this).removeClass('on');
      $(this).addClass('off');
    }

  });

});
