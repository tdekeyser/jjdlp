$(document).ready(function(){
	$("#edit").click(function(e){
		e.preventDefault(e);
		$(".sort").dialog({
			position:{my:"left", at:"right+10 bottom+50", of:"#edit"},
			show: { effect: "toggle", duration: 200 }
		});
	});
});