$(document).ready(function(){

    $(".noteclick").click(function(){
        $(this).removeClass("active");
        $(this).siblings("ul").children("li").slideUp("fast");

        if ($(this).siblings("ul").children("li").is(":hidden")) {
            $(this).addClass("active");
            $(this).siblings("ul").children("li").slideDown("fast");
        }
    });

    $("#gallery_toolbar .button").click(function(){
        if (!$(".noteclick").hasClass("active")) {
            $(".noteclick").addClass("active");
            $(".noteclick").siblings("ul").children("li").slideDown("fast");
        } else {
            $(".noteclick").removeClass("active");
            $(".noteclick").siblings("ul").children("li").slideUp("fast");
        }
    });
});
