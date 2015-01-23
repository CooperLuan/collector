console.log("Hello Weibo");
var s = document.createElement("script");
s.type = "text/javascript";
s.src = "http://cdn.staticfile.org/jquery/2.1.1-rc2/jquery.min.js";
$("head").append(s);

function save_search_result() {
    setTimeout(function() {
        jQuery.ajax({
            url: "http://localhost:8716/",
            type: "POST",
            crossDomain: true,
            data: {
                keyword: jQuery("[class='searchInp_form']").attr("value"),
                route: "weibo.search",
                body: jQuery("[node-type='feed_list']")[0].outerHTML,
                url: window.location.href
            },
            dataType: "json",
            success:function(result){
                jQuery("a[class~='next']")[0].click();
            },
            error:function(xhr,status,error){
                console.log(error);
            }
        });
    }, 2000);
}

function save_comments() {
    if (jQuery("[node-type='comment_detail']")[0] !== undefined) {
        jQuery.ajax({
            url: "http://localhost:8716/",
            type: "POST",
            crossDomain: true,
            data: {
                route: "weibo.comments",
                body: jQuery("[node-type='comment_detail']")[0].outerHTML,
                url: window.location.href
            },
            dataType: "json",
            success: function(result){
                var btn = jQuery("a[class~='next'] span")[0];
                if (btn !== undefined) {
                    jQuery("[comment_id]").remove();
                    btn.click();
                    setTimeout(function() {
                        if (jQuery("[comment_id]").length > 0) {
                            save_comments();
                        }
                    }, 2000);
                } else {
                    fetch_seed();
                }
            },
            error: function(xhr, status, error){
                console.log(error);
            }
        });
    } else {
        // setTimeout(save_comments, 2000);
        fetch_seed();
    }
}

function fetch_seed() {
    jQuery.ajax({
        url: "http://localhost:8716/seed",
        type: "GET",
        crossDomain: true,
        dataType: "json",
        success: function(result) {
            console.log(result);
            if (result.seed !== null) {
                window.location.href = result.seed.url;
            }
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    })
}

if (window.location.host === 's.weibo.com') {
    console.log(window.location.host);
    // save_search_result();
} else {
    console.log(window.location.host);
    setTimeout(function(){
        save_comments();
    }, 2000);
};
