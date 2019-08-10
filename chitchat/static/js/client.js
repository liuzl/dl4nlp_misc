$(document).ready(function() {
    Join();
    $('#submit').click(function() {
        var text = $('#text').val().trim();
        $("#text").val("");
        if (text != "") {
            Parse(text);
        }
    });
    $("#text").on('keypress', function(e) {
        if (e.keyCode != 13) return;
        var text = $('#text').val().trim();
        $("#text").val("");
        if (text != "") {
            Parse(text);
        }
    });
});

function Parse(text) {
    var item = document.createElement("div");
    item.innerHTML = "主人：<font color='yellow'><b>" + text + "</b></font>";
    appendLog(item);

    $.ajax({
        url: "./api?text="+encodeURIComponent(text), cache: false,
        success: function(result) {
            var item = document.createElement("div");
            item.innerHTML = "小灵：<b>" + result["message"] + "</b>";
            appendLog(item);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function appendLog(item) {
    var log = document.getElementById("log");
    var doScroll = log.scrollTop > log.scrollHeight - log.clientHeight - 1;
    log.appendChild(item);
    if (doScroll) {
        log.scrollTop = log.scrollHeight - log.clientHeight;
    }
}

function Join() {
    var item = document.createElement("div");
    item.innerHTML = "小玲：<b>你好，主人！</b>";
    appendLog(item);
}

