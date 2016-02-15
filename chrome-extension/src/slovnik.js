




$( document ).ready(function() {
	var pairs = $('.pair');

	for (var i = 0; i < pairs.length; i++) {
		var p = $(pairs[i]);

		/*var l = "";
		p.find('.l a').each(function(i,e){
			l += $(e).text() + " ";
		});

		var r = "";
		p.find('.r a').each(function(i,e){
			r += $(e).text() + " ";
		});*/
		var l = p.find('.l').text();
		var r = p.find('.r').text();

		l = l.trim();
		r = r.trim();

		var en;
		var cs;

		if(getUrlParameter('dictdir') == "encz.cz"){
			en = r; cs = l;
		} else if(getUrlParameter('dictdir') == "encz.en"){
			en = l; cs = r;
		} else {
			en = ""; cs = "";
		}

		var elem = getButton(en,cs);

		p.append(elem);

	};

});



