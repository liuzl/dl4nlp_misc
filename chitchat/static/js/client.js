$(document).ready(function() {
    var conn;
    var msg = document.getElementById("msg");
    var log = document.getElementById("log");

    function Join() {
        var uid = $("#uid").val().trim();
        if (uid == "") {
            alert("Your uid");
            return;
        }
        if (window["WebSocket"]) {
            conn = new WebSocket("ws://" + document.location.host + "/ws?uid="+encodeURIComponent(uid));
            conn.onclose = function (evt) {
                var item = document.createElement("div");
                item.innerHTML = "<b>Connection closed.</b>";
                appendLog(item);
            };
            conn.onmessage = function (evt) {
                var messages = evt.data.split('\n');
                for (var i = 0; i < messages.length; i++) {
                    var item = document.createElement("div");
                    item.innerText = messages[i];
                    appendLog(item);
                }
            };
        } else {
            var item = document.createElement("div");
            item.innerHTML = "<b>Your browser does not support WebSockets.</b>";
            appendLog(item);
        }
    }

    function appendLog(item) {
        var doScroll = log.scrollTop > log.scrollHeight - log.clientHeight - 1;
        log.appendChild(item);
        if (doScroll) {
            log.scrollTop = log.scrollHeight - log.clientHeight;
        }
    }

    document.getElementById("form").onsubmit = function () {
        if (!conn) {
            alert("Join first");
            return false;
        }
        if (!msg.value) {
            return false;
        }
        conn.send(msg.value);
        msg.value = "";
        return false;
    };
    $('#submit').click(function() {
        Join();
    });
    $("#name").on('keypress', function(e) {
        if (e.keyCode != 13) return;
        Join();
    });
});


