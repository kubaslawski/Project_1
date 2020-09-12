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

function SwitchInbox() {
    var target = event.target || event.srcElement;
    var inbox = document.getElementById('message_inbox')
    var starred = document.getElementById('starred_inbox')
    var important = document.getElementById('important_inbox')
    var sent = document.getElementById('sent_inbox')
    if(target.id == 'inbox_id_1'){
        inbox.hidden = false  
        starred.hidden = true
        important.hidden = true  
        sent.hidden = true  
        //5
        //6
        return 
    }
    if(target.id == 'inbox_id_2'){
        inbox.hidden = true  
        starred.hidden = false
        important.hidden = true  
        sent.hidden = true  
        //5
        //6
        return 
    }
    if(target.id == 'inbox_id_3'){
        inbox.hidden = true  
        starred.hidden = true
        important.hidden = false  
        sent.hidden = true  
        //5
        //6
        return 
    }
    if(target.id == 'inbox_id_4'){
        inbox.hidden = true  
        starred.hidden = true
        important.hidden = true  
        sent.hidden = false  
        //5
        //6
        return 
    }
}

function TestFunc() {
    console.log('TEST')
  
  }