$(function(){
    var $ul = $("#chat");
    var $msg = $("#msg");
    var $clock = $("#clock");
    var clock = new io.Socket(window.location.hostname, {
        "port": 8000,
        "resource": "clock"
    });
    clock.connect();

    clock.addEvent('connect', function(time){
        updateClock(time);
    });

    clock.addEvent('message', function(time){
        updateClock(time);
    });

    var updateClock = function(value){
        $clock.text(value);
        setTimeout(function(){
            clock.send($clock.text());
        }, 1000);
    };

    var socket = new io.Socket(window.location.hostname, {
        "port": 8000,
        "resource": "chat"
    });

    socket.connect();
    socket.addEvent('connect', function() {
        updateClock();
    });

    socket.addEvent('message', function(data) {
        switch (data.type) {
        case "message":
            var li = '<li class="green awesome large">'+data.at+' : '+data.msg+'</li>';
            var contents = $ul.html() + li;
            $ul.html(contents);
            break;
        case "info":
            $.gritter.add({
                title: 'System Information',
                text: data.msg,
                image: '/static/imgs/bot.jpg',
                sticky: false,
                time: 5000,
                class_name: 'sys-info',
                before_open: function(){},
                after_open: function(e){},
                before_close: function(e, manually_closed){},
                after_close: function(){}
            });
            break;
        }
    });

    $("#send").click(function(){
        var msg = $.trim($msg.val());
        if (msg.length == 0) {
            return;
        }
        socket.send(msg);
        $msg.val("");
        return false;
    });

});