"use strict";

$(".top-bar").on(":initpage", function(e) {
    $("#setting").find("[ui-header-setting-user] input").val(settings.user());
    $(this).find("[user-name-menu]").text(settings.user());
});

$("#setting").find("form").submit(function() {
    var page=$(this);

    var user=page.find("[ui-header-setting-user] input").val().toLowerCase();
    settings.user(user);
    $(".top-bar").find("[user-name-menu]").text(user);
    $("#player").trigger(":update");
    return false;
});

var settings={
    user: function (name) {
        if (typeof name != "undefined") localStorage.user=name;
        return typeof localStorage.user!="undefined"?localStorage.user:"guest";
    },
}
