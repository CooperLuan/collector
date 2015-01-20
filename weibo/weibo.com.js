console.log("Hello Weibo");
var s = document.createElement("script");
s.type = "text/javascript";
s.src = "http://cdn.staticfile.org/jquery/2.1.1-rc2/jquery.min.js";
$("head").append(s);

setTimeout(function() {
    var html = jQuery("[node-type='feed_list']")[0].outerHTML;

    jQuery.ajax({
        url: "http://localhost:8716/",
        type: "POST",
        crossDomain: true,
        data: {
            route: "weibo.search",
            body: html,
            url: window.location.href
        },
        dataType: "json",
        success:function(result){
            $("a[class~='next']")[0].click();
        },
        error:function(xhr,status,error){
        }
    });
}, 2000);
