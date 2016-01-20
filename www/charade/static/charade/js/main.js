$(document).ready(function(){
    $("#quote").hide();
    $("#help").hide();
    $("#amount").focus();
    $("#tips1").click(function(){
        $("#quote").slideToggle("slow");
    });
    $("#tips2").click(function(){
        $("#help").fadeToggle("slow");
    });

    $("#ready2go").click(function(){
        var n = $("#amount").val();
        var r = /^[0-9]*$/;
        if(!n){
            event.preventDefault();
            $("#warning").hide();
            $("#warning").text("Set the number before you can play.").slideDown('slow');
            $("#amount").focus();
        }
        else if (!r.test(n)){
            event.preventDefault();
            $("#warning").hide();
            $("#warning").text("Digit only. The value you set '" + n + "' is not valid.").slideDown('slow');
            $("#amount").focus();
        }
        else {
            $("#warning").hide();
            $("#warning").text("Ready!").fadeIn(2000).fadeOut(1000,function(){
                $("#warning").text("Set!").fadeIn(2000).fadeOut(1000,function(){
                    $("#warning").text("Go!").fadeIn(2000).fadeOut(1000,function(){
                        $("#setting").submit();
                    });
                });
            });
        }
    });
});
