function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}


$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function SwitchInstitution() {
  var target = event.target || event.srcElement;
  var id = target.id
  var slide1 = document.getElementById("pagination_div_1")
  var slide2 = document.getElementById("pagination_div_2")
  var slide3 = document.getElementById("pagination_div_3")
  if(target.id == 'pag_li_1'){
    slide1.className = "btn help--slides active"
    slide2.className = "btn help--slides"
    slide3.className = "btn help--slides"
    return
  }
  if(target.id == 'pag_li_2'){
    slide1.className = "btn help--slides"
    slide2.className = "btn help--slides active"
    slide3.className = "btn help--slides"
    return
  }
  if(target.id == 'pag_li_3'){
    slide1.className = "btn help--slides"
    slide2.className = "btn help--slides"
    slide3.className = "btn help--slides active"
    return
  }
}