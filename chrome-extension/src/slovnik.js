
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function getButton(en,cs){
	function addPair(en,cs){
		var str = en + "=" + cs;

		var a = encodeURIComponent(str);

		var url = "http://127.0.0.1:8000/add?text="+a+"&pass=abc";

		$.ajax({
			url: url,
			  cache: false
		}).done(function( html ) {
		    //$( "#results" ).append( html );
		    console.log("Uploaded with message: " + html);

		    if(html == "succ")
		    	alert("Successfully added into wordlist!\n\nEnglish: "+en+"\nCzech: "+cs);
		    else
		    	alert("Error occured ("+html+").");
		  });

	}

	var elem = $('<button/>',
    {
        text: '',
        class: 'brain-btn',
        click: function () { addPair($(this).attr('en'), $(this).attr('cs')); }
    });

	$(elem).attr('en',en);
	$(elem).attr('cs',cs);

	$(elem).css('background-image','url('+chrome.extension.getURL('icons/brain16.png')+')')
	return elem;

}




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



