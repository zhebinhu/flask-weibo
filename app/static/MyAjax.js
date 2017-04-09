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
            alert(typeof data);
            if(data.result)
            {
                if(data.counts) {
                    $(obj).text("取消赞"+"("+data.counts+")");
                    $(obj).css("text-decoration", "none");
                    $(obj).css("color", "#b3b3b3");
                }
                else
                {
                    $(obj).text("取消赞");
                    $(obj).css("text-decoration", "none");
                    $(obj).css("color", "#b3b3b3");
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
                    $(obj).css("color", "#b3b3b3");
                }
                else {
                    $(obj).text("点赞");
                    $(obj).css("text-decoration", "none");
                    $(obj).css("color", "#b3b3b3");
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

$(function () { $('#collapseTwo').collapse('show')});
$(function () { $('#collapseThree').collapse('show')});
$(function () { $('#collapseOne').collapse('show')});

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
                location.href="{{ url_for('auth.login') }}";
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





