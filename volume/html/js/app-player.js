"use strict";

var settings={
    user: function (name) {
        if (typeof name != "undefined") localStorage.user=name;
        return typeof localStorage.user!="undefined"?localStorage.user:"guest";
    },
}
settings.user('user')

function hls_play(page, video, url) {
    if (Hls.isSupported()) {
        var config = {
            xhrSetup: function(xhr, url) {
                xhr.setRequestHeader("X-USER", settings.user());
            }
        };
        var player=new Hls(config);
        player.loadSource(url);
        player.attachMedia(video);
        player.on(Hls.Events.MANIFEST_PARSED,function () {
            video.play();
        });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src= url;
        video.addEventListener('canplay', function() {
            video.play();
        });
    }

    page.unbind(":close").on(":close", function (e) {
        video[0].src='';
        if (typeof(video[0].pause)==='function') video[0].pause();
    });
}

function dash_play(page, video, url) {
    var player=dashjs.MediaPlayer().create();
    player.extend("RequestModifier", function () {
        return {
            modifyRequestHeader: function (xhr) {
                xhr.setRequestHeader("X-USER",settings.user());
                return xhr;
            },
            modifyRequestURL: function (url) {
                return url;
            }
        };
    },true);

    player.initialize();
    player.attachView(video[0]);
    player.attachSource(url);

    page.unbind(":close").on(":close", function (e) {
        player.attachSource(null);
    });
}

//$("#pause").on(":click", function (e) {
var videoInit = function(){
    var url = $("#player video").attr("src")	
    var page=$(this);
    if (url.endsWith(".m3u8") || url.endsWith(".M3U8")) {
        hls_play(page, video, url);
    }
    if (url.endsWith(".mpd") || url.endsWith(".MPD")) {
        dash_play(page, video, url);
    }
};
window.onload = videoInit();
