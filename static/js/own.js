/**
 * Created by kang on 2/26/17.
 */

function own_delete_post(arg) {
  CreateXMLHttpRequest();
  xmlhttp.open("POST", "http://cabana.tech/delete", true);
  xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");  //用POST的时候一定要有这句
  xmlhttp.send("post_id="+arg);

}

function CreateXMLHttpRequest() {
  if (window.ActiveXObject) {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  else if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  }
}