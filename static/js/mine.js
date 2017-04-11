/**
 * Created by kang on 2/26/17.
 */

function own_delete_post(arg) {
    $.post("/delete", {post_id: arg}, function (data, textStatus) {
        window.location.href = ""
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