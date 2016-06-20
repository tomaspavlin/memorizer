var getDefaultOptions = function(){
	var ret = {};
	ret.memorizerServer = "http://ironbrain.net:8000";
	ret.password = "kopretinka382"
	return ret;
};

var getOptions = function(){
	var ret = getDefaultOptions();
	if (localStorage['memorizerServer'] !== undefined)
		ret.memorizerServer = localStorage['memorizerServer']
	if (localStorage['password'] !== undefined)
		ret.password = localStorage['password']
	return ret;
};

var getUrlParameter = function(sParam) {
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

var showNotification = function(title, message){
	chrome.extension.sendRequest({ f: "showNotification", args: [title, message]});
};

var uploadItem = function(str){
	chrome.extension.sendRequest({ f: "uploadItem", args: [str]});
};

var showPromptAndUpload = function (str){
	if(str === undefined) str = "";

	str = prompt("<english> = <definition>",str);
	if(str == null) return;

	uploadItem(str);
};

var getButton = function(en,cs){
	en = en.trim();
	cs = cs.trim();
	en = en.replace("=","-");
	cs = cs.replace("=","-");

	var elem = $('<button/>',
    {
        text: '',
        class: 'brain-btn',
        click: function () { showPromptAndUpload($(this).attr('en') + ' = ' + $(this).attr('cs')); }
    });

	$(elem).attr('en',en);
	$(elem).attr('cs',cs);

	$(elem).css('background-image','url('+chrome.extension.getURL('icons/brain16.png')+')')
	return elem;
};
