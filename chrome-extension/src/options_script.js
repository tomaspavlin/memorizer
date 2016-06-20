var save = function(){
	localStorage['memorizerServer'] = $("#memorizerServer").val();
	localStorage['password'] = $("#password").val();
	
	alert("Saved.");
};

var restore = function(){
	var options = getOptions();
	$("#password").val(options.password);
	$("#memorizerServer").val(options.memorizerServer);
};

var defaults = function(){
	var options = getDefaultOptions();
	$("#password").val(options.password);
	$("#memorizerServer").val(options.memorizerServer);
};

$(document).ready(function(){
	$("#save").click(function(){
		save();
	});
	$("#restore").click(function(){
		restore();
	});
	$("#defaults").click(function(){
		defaults();
	});

	restore();

});
