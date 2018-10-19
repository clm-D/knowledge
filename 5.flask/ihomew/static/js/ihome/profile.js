function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function getUserInfo(){
    $.ajax({
        url: '/user/profile_get/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            if(data.code == '200'){
                if(data.user_avatar){
                    $('#user-avatar').attr('src', '/static/media/' + data.user_avatar);
                }
                if(data.username){
                    $('#user-name').val(data.username);
                }
            }
        },
        error: function(data){
            alert('失败')
        }
    })
}


$(document).ready(function(){
    getUserInfo()

    $('#form-avatar').submit(function (e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/profile/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                if(data.code =='200'){
                    $('#user-avatar').attr('src', '/static/media/' + data.avatar)
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });

    $('#form-name').submit(function(e){
        e.preventDefault()
        var name = $("#user-name").val();
        console.log(name)
        if(name){
            $.ajax({
                url: '/user/profile/',
                type: 'PATCH',
                dataType: 'json',
                data: {'name': name},
                success: function(data){
                    if(data.code == '200'){
                        alert('用户名修改成功')
                        $('#user-name').val(data.name)
                    }else{
                        $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg);
                        $('.error-msg').show()
                    }
                },
                error: function(data){
                    alert('请求失败');
                }
            })
        }
    });

})


