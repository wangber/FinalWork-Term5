function loadMoreGlobalData(){
    $(".givetext").html("正在分析......")
    var sendata = $("#textcon").val();
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/textemotion/",
        data: {
            "text":sendata
        },
        success: function(res) {
            $('.emotion').html(res);
            $(".givetext").html("提交分析")
        }
      });
}
