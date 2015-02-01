function extract_ets_words() {
	var title = $(".ets-ui-acc-step-title span").text();
	var word_nodes = $("div.ets-word-list ul .ets-word");
	var words = [];
	for (var i = 0; i < word_nodes.length; i++) {
		words.push(word_nodes[i].outerText);
	};
	return {
		title: title,
		words: words,
	};
}

function extract_lpn_section() {
	var title = $(".ets-ui-acc-step-title span").text();
	var nodes = $(".ets-act-lpn-section table td");
	var words = [];
	for (var i = 0; i < nodes.length; i++) {
		var text = nodes[i].outerText.trim();
		if (text !== "") {
			words.push(text);
		};
	};
	return {
		title: title,
		words: words,
	};
}

function extract_play_sentences() {
	var title = $(".ets-ui-acc-step-title span").text();
	var words = $(".ets-act-lnc-play-sentences .ets-act-lnc-play-original").text();
	return {
		title: title,
		words: words,
	}
}

function post_data(data) {
	jQuery.ajax({
		url: "http://localhost:8716/",
		type: "POST",
		crossDomain: true,
		data: {
			route: "ec.ef.com.cn",
			body: data,
			url: window.location.href,
			title: $("title").text(),
		},
		dataType: "json",
		success: function(result) {
			console.log(result);
		},
		error: function(xhr, status, error) {
			console.log(error);
		}
	});
}

function run_all() {
	var funcs = [
		extract_ets_words,
		extract_lpn_section,
		extract_play_sentences,
	];
	for (var i = 0; i < funcs.length; i++) {
		var data = funcs[i]();
		if (data.words.length > 0) {
			post_data(data);
		}
	};
}

function insert_button() {
	if ($("#btn-dotjs").length > 0) {
		return;
	}
	var btn = $("<input/>", {
		text: "CLICK ME",
		id: "btn-dotjs",
		style: "position: absolute; right: 0px; top: 50%; z-index: 999; height: 35px;",
	});
	$("body").append(btn);
	$("#btn-dotjs").click(run_all);
}

setInterval(insert_button, 3000);