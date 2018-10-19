function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getUserInfo(){
    $.get('/user/auth_get/', function(data){
        if(data.code == '200'){
            if(data.user.id_name){
                $('#real-name').val(data.user.id_name)
            }
            if(data.user.id_card){
                $('#id-card').val(data.user.id_card)
            }
            if(data.user.id_name && data.user.id_card){
                $("#btn-success").hide();
            }
        }
    })
}


$(document).ready(function(){
    getUserInfo()

    $('#form-auth').submit(function(e){
        e.preventDefault();
        read_name = $('#real-name').val()
        id_card = $('#id-card').val()
        $.ajax({
            url: '/user/auth_post/',
            dataType: 'json',
            type: 'POST',
            data: {'read_name': read_name, 'id_card': id_card},
            success: function(data){
                alert('实名认证成功')
                location.href = '/user/my/'
            },
            error: function(data){
                alert('认证失败')
            }
        })
    })
})