$(function() {
  // standings table
  var $standingson = $('#standings-on');
  var $standingsoff = $('#standings-off');

  $standingson.click(function() {
      $(this).hide();
      $('.standings').toggle("slide", { direction: "right" }, 500);
      $standingsoff.show(500);
    });
  $standingsoff.click(function() {
    $(this).hide();
    $('.standings').toggle("slide", { direction: "right" }, 500);
    $standingson.show(500);
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
  //Filter
  // $('.pool-filter').click(function(){
  //   var index = $(this).parent().index();
  //
  //   $(this).parent().parent().siblings().eq(index+1).toggle();
  //
  //   var $pool = "#pool" + (index+1);
  //
  //   $pool = $($pool);
  //
  //   $pool.next().toggle("slide", {direction:"up"}, 500);
  //   if ($pool.is('.off')){
  //     $pool.removeClass('off');
  //     $pool.addClass('on');
  //   }
  //   else{
  //     $pool.removeClass('on');
  //     $pool.addClass('off');
  //   }
  //
  // });

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
