$(function() {
  //League report score

  $('.report-lscore').click(function(){
    var $score1 = $(this).siblings('input[name=score1]').val();
    var $score2 = $(this).siblings('input[name=score2]').val();
    var $gameno = $(this).siblings('input[name=game-no]').val();
    var $matchid = $(this).siblings('input[name=match-id]').val();
    var $leagueid = $(this).siblings('input[name=league-id]').val();


    if((($score1 >= 21 || $score2 >= 21) && Math.abs($score1 - $score2) >= 2) || ($score1 == 25 || $score2 == 25) ){

      $.ajax({
        url: '/league/reportleaguescore',
        data: {
          'score1': $score1,
          'score2': $score2,
          'game-no': $gameno,
          'match-id': $matchid,
          'league-id':$leagueid
        },
        dataType: 'json',
        success: (json) => { //(json) lets us use $this in success function
          //show the reported score here
          $score = $(this).parent().next();
          $score.children().eq(1).text($score1);
          $score.children().eq(2).text($score2);
          if($score1 > $score2){
            $score.children().eq(1).attr('style', 'font-weight: bold !important');
            $score.children().eq(2).attr('style', 'font-weight: normal !important; padding-top:15px;');
          }
          else{
            $score.children().eq(1).attr('style', 'font-weight: normal !important');
            $score.children().eq(2).attr('style', 'font-weight: bold !important; padding-top:15px;');
          }
          $score.show();

          $(this).parent().hide();
        }
      });

    }
    else{
      alert("Not a valid score. One team must have 21 points and there must be a point differential of 2 or more.");
    }
  });

  $('.update-lscore').click(function(){
    var $score1 = $(this).siblings('input[name=score1]').val();
    var $score2 = $(this).siblings('input[name=score2]').val();
    var $gameno = $(this).siblings('input[name=game-no]').val();
    var $matchid = $(this).siblings('input[name=match-id]').val();
    var $leagueid = $(this).siblings('input[name=league-id]').val();


    if((($score1 >= 21 || $score2 >= 21) && Math.abs($score1 - $score2) >= 2) || ($score1 == 25 || $score2 == 25) ){

      $.ajax({
        url: '/league/updateleaguescore',
        data: {
          'score1': $score1,
          'score2': $score2,
          'game-no': $gameno,
          'match-id': $matchid,
          'league-id':$leagueid
        },
        dataType: 'json',
        success: (json) => { //(json) lets us use $this in success function
          //show the reported score here
          $score = $(this).parent().next();
          $score.children().eq(1).text($score1);
          $score.children().eq(2).text($score2);
          if($score1 > $score2){
            $score.children().eq(1).attr('style', 'font-weight: bold !important');
            $score.children().eq(2).attr('style', 'font-weight: normal !important; padding-top:15px;');
          }
          else{
            $score.children().eq(1).attr('style', 'font-weight: normal !important');
            $score.children().eq(2).attr('style', 'font-weight: bold !important; padding-top:15px;');
          }
          $score.show();

          $(this).parent().hide();
        }
      });

    }
    else{
      alert("Not a valid score. One team must have 21 points and there must be a point differential of 2 or more.");
    }
  });

  $('.update').click(function(){
    var $origscore1 = $(this).siblings('span[name=score1-text]').text();
    var $origscore2 = $(this).siblings('span[name=score2-text]').text();

    $(this).parent().hide();
    var $report = $(this).parent().prev();

    $report.children('input[name=score1]').val($origscore1);
    $report.children('input[name=score2]').val($origscore2);
    $report.children('button[name=update-score]').show();
    $report.children('button[name=report-score]').hide();
    $report.show();

  });

  $('.close').click(function(){
    location.reload();
  });
});
