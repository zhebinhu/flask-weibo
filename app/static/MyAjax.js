/**
 * Created by huzhebin on 17-4-6.
 */
/*异步点赞*/
$(".login-in-like").click(function(){
    params={'id':$(this).attr("post_id")};
    var obj = $(this);
    if($(this).text().match("点赞*")!=null)
    {
        $.getJSON($SCRIPT_ROOT+'/like',params,function(data,status){
            if(data.result)
            {
                if(data.counts) {
                    $(obj).text("取消赞"+"("+data.counts+")");
                    $(obj).css("text-decoration", "none");
                }
                else
                {
                    $(obj).text("取消赞");
                    $(obj).css("text-decoration", "none");
                }
            }
      });
    }
    else
    {
        $.getJSON($SCRIPT_ROOT+'/unlike',params,function(data,status){
            if(data.result)
            {
                if(data.counts) {
                    $(obj).text("点赞"+"("+data.counts+")");
                    $(obj).css("text-decoration", "none");
                }
                else {
                    $(obj).text("点赞");
                    $(obj).css("text-decoration", "none");
                }
            }
        });
    }
    return false;
});

$("#login-email").focus(function () {
      $("#login-email-message").hide();
    });
$("#login-password").focus(function () {
    $("#login-password-message").hide();
});
$("#register-email").focus(function () {
    $("#register-email-message").hide();
});
$("#register-username").focus(function () {
    $("#register-username-message").hide();
});
$("#register-password").focus(function () {
    $("#register-password-message").hide();
});
$("#register-password2-message").focus(function () {
    $("#register-password2-message").hide();
});


$(function () {
    var $frm = $("#login-form");
    $frm.submit(function (ev) {
    $.ajax({
        type: $frm.attr('method'),
        url: $frm.attr('action'),
        data: $frm.serialize(),
        success: function (data) {
            if(data.result)
            {
                location.reload();
            }
            else
            {
                $("#login-email-message").hide();
                $("#login-password-message").hide();
                if(data.errors.email) {
                    $("#login-email-message").text(data.errors.email);
                    $("#login-email-message").show();
                }
                else if(data.errors.password) {
                    $("#login-password-message").text(data.errors.password);
                    $("#login-password-message").show();
                }
            }
        }

    });
    ev.preventDefault();

});
});

$(function () {
    var $frm = $("#register-form");
    $frm.submit(function (ev) {
    $.ajax({
        type: $frm.attr('method'),
        url: $frm.attr('action'),
        data: $frm.serialize(),
        success: function (data) {
            if(data.result)
            {
                location.reload();
            }
            else
            {
                $("#login-email-message").hide();
                $("#login-username-message").hide();
                $("#login-password-message").hide();
                $("#login-password2-message").hide();
                if(data.errors.email) {
                    $("#register-email-message").text(data.errors.email);
                    $("#register-email-message").show();

                }
                else if(data.errors.username)
                {
                    $("#register-username-message").text(data.errors.username);
                    $("#register-username-message").show();
                }
                else if(data.errors.password) {
                    $("#register-password-message").text(data.errors.password);
                    $("#register-password-message").show();
                }
                else if(data.errors.password2)
                {
                    $("#register-password2-message").text(data.errors.password2);
                    $("#register-password2-message").show();
                }
            }
        }

    });
    ev.preventDefault();

});
});
$(
  function () {
      var url = location.href;
      if(url.indexOf("/user")!=-1)
      {
          $("body").css("background-color","#f7f8fa");
      }
      if(url.indexOf("/index")!=-1)
      {
          $("body").css("background","url('../static/image/beijing.jpg') center top no-repeat fixed");
          var $width = document.body.clientWidth;
      }
  }
);

$(
  function () {
     for(var i=3;i<$("[focus='focus']").size();i++) {
         $($("[focus='focus']")[i]).hide();
     }
     $("#displaymore").click(
         function () {
             if($("#displaymore").text().indexOf("查看更多")!=-1) {
                 $("#displaymore").html("<a style='cursor: pointer;color: #888888'>收回</a>");
                 for (var i = 3; i < $("[focus='focus']").size(); i++) {
                     $($("[focus='focus']")[i]).slideDown();
                 }
             }
             else{
                  $("#displaymore").html("<a style='cursor: pointer;color: #888888'>查看更多</a>");
                 for (var i = 3; i < $("[focus='focus']").size(); i++) {
                     $($("[focus='focus']")[i]).slideUp();
                 }
             }
         }
     );
  }
);

$(function () {
     $("html").mousedown(function () {
        if($(".mobile-inner-nav").is($(":visible")))
        {
            var div = $(".mobile-inner-nav:visible").get(0);
            if(div.contains(window.event.srcElement))
            {

            }
            else
            {
                $(".mobile-inner-nav").hide();
            }
        }
    });
})
$(".mobile-inner-header-icon").click(function(){
    var post_id = $(this).attr('post_id');
    $(this).toggleClass("mobile-inner-header-icon-click mobile-inner-header-icon-out");
    $(".mobile-inner-nav[post_id="+post_id+"]").slideToggle(250);
});

$(".mobile-inner-nav a").each(function( index ) {
    $( this ).css({'animation-delay': (index/10)+'s'});
});

$(document).ready(function(){
    $("a#func1").click(function(){
        $("div#line-1").animate({left:'29px'});
        $("div#user_shoucang").hide();
        $("div#user_guanzhu").hide();
        $("div#user_fensi").hide();
        $("div#user_weibo").show();
    });
    $("a#func2").click(function(){
        $("div#line-1").animate({left:'119px'});
        $("div#user_weibo").hide();
        $("div#user_guanzhu").hide();
        $("div#user_fensi").hide();
        $("div#user_shoucang").show();
    });
    $("a#func3").click(function(){
        $("div#line-1").animate({left:'209px'});
        $("div#user_weibo").hide();
        $("div#user_shoucang").hide();
        $("div#user_fensi").hide();
        $("div#user_guanzhu").show();
    });
    $("a#user_guanzhu_1").click(function(){
        $("div#line-1").animate({left:'209px'});
        $("div#user_weibo").hide();
        $("div#user_shoucang").hide();
        $("div#user_fensi").hide();
        $("div#user_guanzhu").show();
    });
    $("a#func4").click(function(){
        $("div#line-1").animate({left:'299px'});
        $("div#user_weibo").hide();
        $("div#user_shoucang").hide();
        $("div#user_guanzhu").hide();
        $("div#user_fensi").show();
    });
    $("a#user_fensi_1").click(function(){
        $("div#line-1").animate({left:'299px'});
        $("div#user_weibo").hide();
        $("div#user_shoucang").hide();
        $("div#user_guanzhu").hide();
        $("div#user_fensi").show();
    });
});

$(function () { $('#collapseOne').collapse('show')});
$(function () { $('#collapseTwo').collapse('show')});
$(function () { $('#collapseThree').collapse('show')});


//关注和取消关注
function over(obj) {
if(obj.innerHTML=="关注") {
    $(obj).css("background-color","#0D79D1");
}
if(obj.innerHTML=="已关注") {
    obj.innerHTML = "取消关注";
    $(obj).css("background-color","rgb(171, 182, 197)");
}
if(obj.innerHTML=="已收藏") {
    obj.innerHTML = "取消收藏";
}
}

function out(obj) {
if(obj.innerHTML=="关注") {
    $(obj).css("background-color","rgb(15, 136, 235)");
}
if(obj.innerHTML=="取消关注") {
    obj.innerHTML = "已关注";
    $(obj).css("background-color","rgb(195, 204, 217)");
}
if(obj.innerHTML=="取消收藏") {
    obj.innerHTML = "已收藏";
}
}

$(function () {
     /*异步收藏*/
$(".login-in-collect").click(function () {
    params = {'id': $(this).attr("post_id")};
    var obj = $(this);
    if ($(obj).text() == "收藏") {
        $.getJSON($SCRIPT_ROOT + '/collect', params, function (data, status) {
            if (data.result) {
                $(obj).text("已收藏");
                $(obj).removeClass("glyphicon-star-empty")
                $(obj).addClass("glyphicon-star wb-post-footer login-in-collect");
                //text1 += "已收藏";
            }
        });
    }
    else {
        $.getJSON($SCRIPT_ROOT + '/uncollect', params, function (data, status) {
            if (data.result) {
                $(obj).text("收藏");
                $(obj).removeClass("glyphicon-star");
                $(obj).addClass("glyphicon glyphicon-star-empty wb-post-footer login-in-collect");
                //text1 += "收藏";
            }
        });
    }
});
})


/*话题功能实现*/
function ReplaceTopic(str){
    var t, k, r, u;   // 声明变量。
    str = str.replace("&nbsp;"," ")
    var ss = str;
    t=ss.replace(/\#([^\#|.]+)\#/g, function(word){
        k = word.replace(/\#/g,"");
        return "<a  style=\"cursor: pointer\" href='"+$SCRIPT_ROOT+'/index/topic?topic='+k+"'>" + word + "</a>";
        }
    );
    r=t.replace(/\@([^\@(</p>)|.]+?)\s/g, function (word) {
        u = word.replace(/\@/g,"");
        return "<a style=\"cursor: pointer\" href='"+$SCRIPT_ROOT+'/relate?username='+u+"'>" + word + "</a>";
    })
    return(r);  //返回替换后的字符串
}

$(".replace_body").show(function () {
    var str = $(this)[0].innerHTML;
    var s = ReplaceTopic(str);
    $(this)[0].innerHTML=s;
})

$("a#followeds_guanzhu").click(function () {
    params={'username':$(this).attr("username")};
    var obj = $(this);
    if($(this).text()=="关注")
    {
        $.getJSON($SCRIPT_ROOT+'/follow',params,function(data,status){
            if(data.result)
            {
                if(obj.attr("sign")!=null)
                {
                    $(".followers_count").text(data.count)
                }
                $(obj).text("已关注");
                $(obj).css("background-color","rgb(195, 204, 217)");
            }
        });
    }
    else
    {
        $.getJSON($SCRIPT_ROOT+'/unfollow',params,function(data,status){
            if(data.result)
            {
                if(obj.attr("sign")!=null)
                {
                    $(".followers_count").text(data.count)
                }
                $(obj).text("关注");
                $(obj).css("background-color","rgb(15, 136, 235)");
            }
        });
    }
})


//评论检测字数功能
$(function () {
    $(document).on(
        "input",
        "#body",
        function () {
            var length = $("#body").val().length;
            if(length>99||length==0)
            {
                $("#commentNum").html("<span>已输入<font style='color:red;font-size:18px;font-family:Constantia, Georgia;'>"+length+"</font>个字</span>");
                $("#submit").attr("disabled","true");
                //$("#s").removeClass("W_btn_a");
                //$("#sharebutton").addClass("W_btn_b");
            }
            else{
                $("#commentNum").html("<span>已输入<font style='font-size:18px;font-family:Constantia, Georgia;'>"+length+"</font>个字</span>");
                $("#submit").removeAttr("disabled");
                //$("#sharebutton").removeClass("W_btn_b");
                //$("#sharebutton").addClass("W_btn_a");
            }
        }
    );
})





