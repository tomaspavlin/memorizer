

$(document).ready(function(){
	$("#form").submit(function(){
		var text = $("#text").val();
		uploadItem(text);

		window.close();
		return false;
	});


})