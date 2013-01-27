function sentenceById() {
    var element = document.getElementById("SentenceQuery");
    var result = foo.sentenceById(element.value);
    var text = document.getElementById("text");
    text.innerHTML = "<a dir=\"ltr\" class=\"text\">" + result + "</a>";
}
function translationById() {
    var element = document.getElementById("SentenceQuery");
    var result = foo.translationById(element.value);
    var traduko = document.getElementById("multi");
    var e = result.split("\n");
    for (i = 0; i < e.length; i += 1) 
	traduko.innerHTML += "<p>" + e[i] + "</p>";
}
function sentencesByRegex() {
    var element = document.getElementById("SentenceQuery");
    var result = foo.sentencesByRegex(element.value);
    var text = document.getElementById("multi");
    var e = result.split("\n");
    for (i = 0; i < e.length; i += 1) 
	text.innerHTML += "<p>" + e[i] + "</p>";
}
