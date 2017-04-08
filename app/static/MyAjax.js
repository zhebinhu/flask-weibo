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




