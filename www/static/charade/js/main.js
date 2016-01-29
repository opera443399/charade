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

    function ready_set_go(){
        var n = $("#amount").val();
        var r = /^[0-9]*$/;
        if(!n){
            event.preventDefault();
            $("#warning").hide();
            $("#warning").text("Set the number before you can play.").slideDown('slow');
            $("#amount").focus();
        }
        else if(!r.test(n)){
            event.preventDefault();
            $("#warning").hide();
            $("#warning").text("Digit only. The value you set '" + n + "' is not valid.").slideDown('slow');
            $("#amount").focus();
        }
        else {
            event.preventDefault();
            $("#warning").hide();
            $("#warning").text("Ready!").fadeIn(1000).fadeOut(1500,function(){
                $("#warning").text("Set!").fadeIn(1000).fadeOut(1500,function(){
                    $("#warning").text("Go!").fadeIn(1000).fadeOut(1500,function(){
                        $("#setting").submit();
                    });
                });
            });
        }
    };

    $("#ready2go").click(function(){
        ready_set_go();
    });

    $("#amount").keydown(function(){
        if(event.keyCode==13){
            console.log("[test] key 'Enter' is pressed.");
            console.log("[test] Let's charade.");
            event.preventDefault();
            ready_set_go();
        }
    });
});
