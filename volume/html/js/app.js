"use strict";

$(document).foundation();
$(window).bind("load", function () {
    $(".top-bar").trigger(":initpage");
    $("#player").trigger(":update");
});
