function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });

    url = location.search
    id = url.split('=')[1]
    $.get('/house/detail_get/' + id + '/', function(data){
        if(data.code == '200'){
            var house = template('house_booking_script', {ohouse: data.house_list})
            $('.house-info').append(house)
        }
    });

    $('.submit-btn').click(function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        data = {'house_id': id, 'start_date': startDate, 'end_date': endDate};
        $.post('/order/booking_post/', data, function(data){
            if(data.code =='200'){
                location.href = '/order/orders/'
            };
            if(data.code == '1101'){
                alert(data.msg);
                location.href = '/user/my/';
            }
        })
    })

    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
})
