//chrome.browserAction.onClicked.addListener(function(tab) {
//	addItem();
//
//});

chrome.extension.onRequest.addListener(function(r, sender, sendResponse){
        if(r.f == "showNotification") showNotification(r.args[0], r.args[1]);
        else if(r.f == "uploadItem") uploadItem(r.args[0]);
        else {
        	console.error("Invalid request.");
        	console.error(r);
        }
});



var showNotification = function(title, message){
	var opt = {
		type: "basic",
		title: title,
		message: message,
		iconUrl: "icons/brain128.png"
	};

	chrome.notifications.create(undefined, opt, function(){});

};


var uploadItem = function(str){
	var showErr = function(msg){
		if(msg === undefined) msg = "";

		if(msg != "")
			showNotification("Error :(", msg);
		else showNotification("Error :(", "");
	};

	if(str === undefined) str = "";
	if(str == null) str = "";
	if(str == "") {
		showErr();
		return;
	}

	str = str.replace(/\n/g,"|");

	var a = encodeURIComponent(str);
	var url = getOptions().memorizerServer + "/add?text="+a+"&pass=abc";

	$.ajax({
		url: url,
		  cache: false
	}).done(function( html ) {
	    console.log("Uploaded with message: " + html);

	    if(html == "succ")
	    	showNotification("Success! :)", "Successfully added into wordlist.");
	    else showErr(html);
	    	
	  }).error(function(e){
	  	showErr("Is http server running?");
	  });
};