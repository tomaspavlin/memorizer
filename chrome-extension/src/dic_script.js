$(document).ready(function(){

	$('#form').submit(function(e){
		e.preventDefault();


		var w = $('#text').val();
		var dictionary_src = "http://www.dictionary.com/browse/" + w;
		var slovnik_src = "http://slovnik.cz/bin/mld.fpl?dictdir=encz.en&lines=30&js=1&vcb=" + w;

		console.log(w);
		console.log(dictionary_src);
		console.log(slovnik_src);

		$('#dictionary-iframe').attr('src', dictionary_src);
		$('#slovnik-iframe').attr('src', slovnik_src);
	});
	
	$('iframe').load(function(){
		$("#text").focus();
	});

	$("#text").focus();
});