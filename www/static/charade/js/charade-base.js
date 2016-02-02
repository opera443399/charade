/* base */
$(document).ready(function(){
    $("#quote").hide();
    $("#help").hide();
    $("#tips1").click(function(){
        $("#quote").slideToggle("slow");
    });
    $("#tips2").click(function(){
        $("#help").fadeToggle("slow");
    });
});
