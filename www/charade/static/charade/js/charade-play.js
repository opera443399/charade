/* test ajax */
function showtime(){
    $.ajax({
        url: "/charade/show/time/",
        type: "GET",
        dataType: "json",
        success: function(showtime){
            $('#showtime').html(showtime.now);
        }
    });
}

$(document).ready(function(){
    setInterval(showtime, 1000);
});
