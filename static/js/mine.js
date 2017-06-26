/**
    * Created by kang
    * on 2/26/17.
    */

// 删除文章
function own_delete_post(arg) {
    $.post("/delete", {post_id: arg},function (result) {
        if(result.isLogin && result.deleted){
            window.location.href='/'
        }else {
            window.location.href='/login'
        }
    })
}

// 旋转菜单js
var $page = $('.page');

$('.menu_toggle').on('click', function () {
    $page.toggleClass('shazam');
});
$('.content').on('click', function () {
    $page.removeClass('shazam');
});

//tagsinput
$('#tags').tagsInput();