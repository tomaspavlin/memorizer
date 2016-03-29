var save = function(){
	localStorage['memorizerServer'] = $("#memorizerServer").val();
	alert("Saved.");
};

var restore = function(){
	var options = getOptions();
	$("#memorizerServer").val(options.memorizerServer);
};

var defaults = function(){
	var options = getDefaultOptions();
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