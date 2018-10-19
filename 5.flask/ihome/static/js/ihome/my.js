function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.get('/user/my_get/', function(data){
        if(data.code == '200'){
            $('#user-name').html(data.username)
            $('#user-mobile').html(data.mobile)
            if(data.avatar){
                $('#user-avatar').attr('src', '/static/media/' + data.avatar)
            }
        }
    })

})