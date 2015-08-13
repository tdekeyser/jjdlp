$(document).ready(function(){
	$("#authorsorter_link").click(function(e){
		e.preventDefault(e);
		$("#author_box").dialog({
			position:{my:"left", at:"right+10 bottom+50", of:"#authorsorter_link"},
			show: { effect: "toggle", duration: 200 }
		});
	});
	$("#titlesorter_link").click(function(e){
		e.preventDefault(e);
		$("#title_box").dialog({
			position:{my:"left", at:"right+10 bottom+50", of:"#titlesorter_link"},
			show: { effect: "toggle", duration: 200 }
		});
	});
	$("#citysorter_link").click(function(e){
		e.preventDefault(e);
		$("#city_box").dialog({
			position:{my:"left", at:"right+10 bottom+50", of:"#citysorter_link"},
			show: { effect: "toggle", duration: 200 }
		});
	});
	$("#datesorter_link").click(function(e){
		e.preventDefault(e);
		$("#date_box").dialog({
			position:{my:"left", at:"right+10 bottom+50", of:"#datesorter_link"},
			show: { effect: "toggle", duration: 200 }
		});
	});
});