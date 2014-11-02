

var votedata=null;



function readData(){
  votedata = d3.csv.parse("./data/votedata.csv");
}



$(function(){
    readData();
    $('body').scrollspy({ target: '#navbar',offset:80 });
    $('#navbar').on('activate.bs.scrollspy', function () {
    //$("li.list-group-item").removeClass("list-group-item-success");
    //$("li.list-group-item.active").addClass("list-group-item-success");
        var offset = $("body").scrollTop() - ( $("#chap1").offset().top-70);
    });

    //移動導覽列位置
    $(document).bind("scroll","body",function(){
        var h = $("#chap1").parent().offset().top;
        var move = h - $("body").scrollTop();
        move = (move>=70)?move:70;
        $('#navbar').css({top: move+"px"});
    });

    //增加底層位置
    $(".footer").css({"height":$(window).height()+"px"});
    //刷新頁面佈局
    $('[data-spy="scroll"]').each(function () {
        var $spy = $(this).scrollspy('refresh');
    });
    //增加






//回到最上頭
    $('a:contains(回頁頭)').click(
      function(){
        $('html,body').animate({scrollTop:0}, 'slow');
        return false;
      }
    );

//跑到其他頁面
 var size = $('.nav_list li').size();
  for(var i =1;i<size;i++){
    $($('.nav_list li')[i]).click(
      function(){
        $('html,body').animate({scrollTop: $($("a",this).attr("href")).offset().top -70 }, 'slow');
        return false;
      }
      );

  }


});
