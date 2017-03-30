/**
 * Created by kang on 2/26/17.
 */

function own_delete_post(arg) {
    CreateXMLHttpRequest();
    xmlhttp.open("POST", "http://cabana.tech/delete", true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");  //用POST的时候一定要有这句
    xmlhttp.send("post_id=" + arg);

}

function CreateXMLHttpRequest() {
    if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    else if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
}

// 旋转菜单js
var $page = $('.page');

$('.menu_toggle').on('click', function () {
    $page.toggleClass('shazam');
});
$('.content').on('click', function () {
    $page.removeClass('shazam');
});

// 分页

layui.use(['laypage'], function () {
    var laypage = layui.laypage;

    laypage({
        cont: 'page_number',
        pages: 100, //总页数
        groups: 5, //连续显示分页数
        skin:"#F37272"
    });
});

// 背景js
