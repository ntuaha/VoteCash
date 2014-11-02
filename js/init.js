



$(function(){
  $('body').scrollspy({ target: '#navbar',offset:80 });
  $('#navbar').on('activate.bs.scrollspy', function () {
    var offset = $("body").scrollTop() - ( $("#chap1").offset().top-70);
  });

//移動導覽
  $(document).bind("scroll","body",function(){
    var h = $("#chap1").parent().offset().top;
    var move = h - $("body").scrollTop();
    move = (move>=70)?move:70;
    $('#navbar').css({top: move+"px"});
  });

// insert footer
  $(".footer").css({"height":$(window).height()+"px"});
// refresh items in the navigation list
  $('[data-spy="scroll"]').each(function () {
    var $spy = $(this).scrollspy('refresh');
  });



//scroll to the top
  $('a:contains(回頁首)').click(
    function(){
      $('html,body').animate({scrollTop:0}, 'slow');
      return false;
    }
  );

//scroll to the specific topic
    var size = $('.nav_list li').size();
    for(var i =1;i<size;i++){
      $($('.nav_list li')[i]).click(
      function(){
        $('html,body').animate({scrollTop: $($("a",this).attr("href")).offset().top -70 }, 'slow');
        ga('send', 'event', 'watch', 'click', $("a",this).text());
        return false;
      });
    };


});
