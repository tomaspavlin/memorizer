




$( document ).ready(function() {
	var pairs = $('.pair');
	var sections = $('section');

	for (var i = 0; i < sections.length; i++) {
		var s = $(sections[i]);

		var title = s.find($(".head-entry"));

		var term = title.text();
		if(term == "") continue;


		defsE = s.find('.def-content');
		console.log(defsE.length);
		for(var j = 0; j < defsE.length; j++){
			var defE = $(defsE[j]);
			if(defE.attr("injected")) continue;
			else defE.attr("injected",true);

			var def = defE.text();

			var elem = getButton(term, def);
			defE.append(elem);

		}

	};

});



