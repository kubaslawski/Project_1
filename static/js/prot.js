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


function updateStatus() {
    var target = event.target || event.srcElement;
    var id = target.id
    $.ajax({
        type: "POST",
        url: "/ajax/taken_or_not_taken/",
        cache: false, 
        data: {
            "donation_number": id
        }
    }).done(function(e){
        console.log("done") 
        var SpanToRemove = document.getElementById('p_'+id)
        var H4_El = document.getElementById('h4_'+id).innerText
        console.log(SpanToRemove)
        if(SpanToRemove.className == "taken"){
           console.log("taken")
           var DivToAppend = document.getElementById("Div_Not_Taken_Id")
           DivToAppend.innerHTML += 
           '<span id="p_"'+id +' class="not_taken">' +
           '<h4 id="h_"'+id +'>'+H4_El+'</h4' +
           '<input id="'+id +'type="button"  onclick="updateStatus()" value="Mark as taken">' +
           '</span>'
        }
        if(SpanToRemove.className =="not_taken"){
            console.log("not_taken")
        }
    })
    .fail(function(e){
        console.log('error')
    })

}
 