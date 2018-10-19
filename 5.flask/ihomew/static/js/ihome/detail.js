function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}


function getInfo(){
    url = location.search
    id = url.split('=')[1]
    url_str = '/house/detail_get/' + id + '/'
    $.get(url_str, function(data){
        if(data.code == '200'){
            var house = template('houst_detail_script', {ohouse: data.house_list})
            $('.container').append(house)

            if(data.house_list.max_days){
                $('#max-days span').html(data.house_list.max_days)
            }else{
                $('#max-days span').html('日期不限')
            }

            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            $(".book-house").show();
        }
    })
}


$(document).ready(function(){
    getInfo()
})