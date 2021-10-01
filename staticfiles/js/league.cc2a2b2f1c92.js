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
  var $togglestandings = $('.standings-container #toggle-standings');
  var $toggleleague = $('#toggle-league');
  var $toggletournament = $('#toggle-tournament');
  $togglestandings.click(function() {
    if ($(this).is('.on')){
      $('.standings').toggle("slide", { direction: "right" }, 1000);
      $('.standings-container').animate({"margin-left": '+=600'}, 500);
      $(this).addClass('off');
      $(this).removeClass('on')
    }
    else if ($(this).is('.off')){
      $('.standings').toggle("slide", { direction: "left" }, 500);
      $('.standings-container').animate({"margin-left": '-=600'}, 500);
      $(this).addClass('on');
      $(this).removeClass('off')
    }
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
