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
    $.get('/user/profile_get/', function(data){
        if(data.icon){
            $('#user-avatar').attr('src', '/static/media/' + data.icon)
        };
        if(data.username){
            $('#user-name').val(data.username)
        }
    })
}


$(document).ready(function(){
    getUserInfo();

    $('#form-avatar').submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/user/profile_patch/',
            type: 'PATCH',
            dataType: 'json',
            success: function(data){
                if(data.code == '200'){
                    alert('修改成功')
                    $('#user-avatar').attr('src', '/static/media/' + data.avatar_url)
                    location.href = '/user/my/'
                }
            },
            error: function(data){
                alert('失败')
            }
        })
    })

    $('#form-name').submit(function(e){
        e.preventDefault()

        $(this).ajaxSubmit({
            url: '/user/profile_patch/',
            type: 'PATCH',
            dataType: 'json',
            success: function(data){
                if(data.code == '200'){
                    alert('修改成功')
                    $('#user-name').val(data.name)
                    location.href = '/user/my/'
                }
            },
            error: function(data){
                alert('失败')
            }
        })
    })

})