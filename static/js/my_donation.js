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
        var SpanToRemove = document.getElementById('p_'+id)
        //console.log(SpanToRemove)
        if(SpanToRemove.className == "taken"){
           //console.log("taken")
           var DivToAppend = document.getElementById("Div_Not_Taken_Id")
           var ActualDiv = document.getElementById("Div_Taken_Id")
           SpanToRemove.className = "not_taken"
           var InputToChange = document.getElementById(id)
           console.log(target)
           InputToChange.value = "Mark as taken"
           //console.log(InputToChange.value)
           SpanToRemove.remove()
           DivToAppend.innerHTML += SpanToRemove.outerHTML
           return 
        }
        if(SpanToRemove.className =="not_taken"){
            var DivToAppend = document.getElementById("Div_Taken_Id")
            var ActualDiv = document.getElementById("Div_Not_Taken_Id")
            SpanToRemove.className = "taken"
            var InputToChange = document.getElementById(id)
            console.log(InputToChange)
            InputToChange.value = "Mark as not taken"
            //console.log(InputToChange.value)
            SpanToRemove.remove()
            DivToAppend.innerHTML += SpanToRemove.outerHTML
            return
        }
    })
    .fail(function(e){
        console.log('error')
    })

}
 