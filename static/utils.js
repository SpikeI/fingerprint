function choose_have_id(choice){
    if(choice){
        new_html = "Plase input your ID:  "
        new_html += '<input id="uid" type="text" name="uid"> ';
        new_html += '<button onclick="button_send()">确定</button>';
        $("#ask_panel").html(new_html);
    }else{
        button_new_user()
    }
}

function button_send(){
    let uid = $("#uid")[0].value;
    let data = fingerprint_data;
    data['uid'] = uid;
    console.log(data);
    $.ajax({
          url : "/fingerprint/features",
          dataType : "json",
          contentType: 'application/json',
          type : 'POST',
          data : JSON.stringify(data),
          success : function(result) {
            $("#status").html("Success");
            window.location.href = "/service";
          },
          error: function (xhr, ajaxOptions, thrownError) {
              $("#status").html("Network Error");
            // alert(thrownError);
          }
        });
}

function button_new_user(){
    let data = fingerprint_data;
    $.ajax({
          url : "/fingerprint/features",
          dataType : "json",
          contentType: 'application/json',
          type : 'POST',
          data : JSON.stringify(data),
          success : function(result) {
            if(result.status === 'new'){
                    let uid = result.uid;
                    set_storage(result.mark);
                    $("#status").html("你的ID是 " + uid + " 在其他浏览器登陆时，请输入这个ID ");
                    $("#ask_panel")[0].hidden = true;
                }else{
                    $("#status").html("你是老用户吗:)<br>你的ID是 " + result.uid);
                    $("#ask_panel")[0].hidden = true;
                }
          },
          error: function (xhr, ajaxOptions, thrownError) {
            alert(thrownError);
          }
        });
}