function loadMoreGlobalData(){
    var sendata = $("#sentence").val();
    $.ajax({
        type: "POST",
        url: "../sentype/",
        data: {
            "sen":sendata
        },
        success: function(res){
            $('.sentype').html(res);
            $('.sencon').html(sendata);
        },
      });
}
