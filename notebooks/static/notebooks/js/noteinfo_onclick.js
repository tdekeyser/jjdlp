
$(document).ready(function(){
    $("#allbutton").click(function(){
        $(".noteinfo").toggle("fast");
    });
    $('#sourcebutton').click(function(){
    	$(".sourceinfo").toggle("fast");
    });
    $('#annotationbutton').click(function(){
    	$(".annotation").toggle("fast");
    });
    $('#msinfobutton').click(function(){
    	$(".msinfo").toggle("fast");
    });
    $('#ctransferbutton').click(function(){
    	$(".ctransfer").toggle("fast");
    });
});