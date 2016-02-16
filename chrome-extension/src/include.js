var memorizerServer = "http://192.168.1.14:8000";

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

var addItem = function (str){
	//var str = en + "=" + cs;
	if(str === undefined) str = "";

	var showErr = function(msg){
		if(msg === undefined) msg = "";

		if(msg != "")
			alert("Error occured: " + msg);
		else alert("Error occured.");
	};

	str = prompt("<english> = <czech>",str);
	if(str == null) return;

	var a = encodeURIComponent(str);

	var url = memorizerServer + "/add?text="+a+"&pass=abc";

	$.ajax({
		url: url,
		  cache: false
	}).done(function( html ) {
	    console.log("Uploaded with message: " + html);

	    if(html == "succ")
	    	alert("Successfully added into wordlist!");
	    else showErr(html);
	    	
	  }).error(function(){
	  	showErr("Is http server running?");
	  });
};

var getButton = function(en,cs){
	var elem = $('<button/>',
    {
        text: '',
        class: 'brain-btn',
        click: function () { addItem($(this).attr('en') + ' = ' + $(this).attr('cs')); }
    });

	$(elem).attr('en',en);
	$(elem).attr('cs',cs);

	$(elem).css('background-image','url('+chrome.extension.getURL('icons/brain16.png')+')')
	return elem;
};