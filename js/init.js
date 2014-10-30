

var votedata=null;

function readData(){
  votedata = d3.csv.parse("./data/votedata.csv");
}



$(function(){
  readData();
  $('body').scrollspy({ target: '.navbar-example',offset:80 });


    $('a.navbar-brand').click(
      function(){
        $('html,body').animate({scrollTop:0}, 'slow');
        return false;
      }
      );


 var size = $('.pull-right  a').size();
  for(var i =0;i<size;i++){
    $($('.pull-right  a')[i]).click(
      function(){
        $('html,body').animate({scrollTop: $($(this).attr("href")).offset().top -70 }, 'slow');
        return false;
      }
      );

  }


});
