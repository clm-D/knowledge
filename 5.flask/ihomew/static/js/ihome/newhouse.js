function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function getHouseInfo(){
    $.get('/house/house_info_get/', function(data){
        if(data.code == '200'){
            for(var i = 0; i < data.area_list.length; i++){
                area_str = '<option value="' + data.area_list[i].id + '">' + data.area_list[i].name + '</option>'
                $('#area-id').append(area_str)
            }

            for(var j = 0; j < data.facility_list.length; j++){
                var facility_str = ''
                facility_str += '<li><div class="checkbox"><label>'
                facility_str += '<input type="checkbox" name="facility" value="' + data.facility_list[j].id +'">' + data.facility_list[j].name
                facility_str += '</label></div></li>'
                $('.house-facility-list').append(facility_str)
            }
        }
    })
}


$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    getHouseInfo()

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/newhouse_post/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                $('#form-house-info').hide()
                $('#form-house-image').show()
                $('#is-sure').hide()
                console.log(data.house_id)
                $('#house-id').val(data.house_id)
            },
            error: function(data){
                alert('失败')
            }
        })
    })

    $('#form-house-image').submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/house/house_image_post/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                if(data.code == '200'){
                    var img_str = '<img src="/static/media/' + data.image_url + '">'
                    $('#is-sure').show()
                    $('.house-image-cons').append(img_str)
                }
            },
            error: function(data){
                alert('图片上传失败')
            }
        })
    })

})