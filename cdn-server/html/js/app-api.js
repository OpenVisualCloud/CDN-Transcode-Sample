"use strict";

var apiHost={
    playList: function (name) {
        var url="api/playlist";
        var args= { name: name };
        console.log("GET "+url+"?"+JSON.stringify(args));
        return $.get(url, args);
    },
    click: function (name, x, y, t) {
        var url="api/click";
        var args= { x: x, y:y, name: name, t:t }
        console.log("POST "+url+"?"+JSON.stringify(args));
        return $.post(url, args);
    },
};
