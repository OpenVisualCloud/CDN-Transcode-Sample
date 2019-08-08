"use strict";

var videogrid = document.querySelector(".video-grid")
var video = document.querySelector("video")
var fullBtn = document.getElementById("maxvideo")
var playBtn=document.getElementById("pause")
var velocity = document.getElementById("velocity")
var duration = $('#duration').attr("name")
var volume = document.getElementById('volume')

var controlSize = function(){
    var height = $('.video-grid-video').outerHeight()
    $('.control').css('marginTop',-height*12/100);
    $('.control').css('height',height*10/100);
}

videogrid.onmouseenter = function (){
    controlSize()
    $(".control").slideDown(200)
};
videogrid.onmouseleave = function (){
    $(".control").slideUp(200)
};

volume.onmouseenter = function(){
    document.querySelector("#volume .progress").style.display='inline-block';
    document.querySelector("#volume .progress-bar").style.display='inline-block';
}
volume.onmouseleave = function(){
    document.querySelector("#volume .progress").style.display='none';
    document.querySelector("#volume .progress-bar").style.display='none';
}
$('#volume span').click(function(){
    if (video.volume == 0){
        video.volume = $("#volume .progress-bar").width()/$("#volume .progress").width()
        $(this).attr('class', 'glyphicon glyphicon-volume-up')
    }else{
        video.volume = 0
        $(this).attr('class', 'glyphicon glyphicon-volume-off')
    }
})

var timeTransformation = function(time){
    var h = Math.floor(time/60);
    var s = time%60;
    h += '';
    s += '';
    h = (h.length==1)?'0'+h:h;
    s= (s.length==1)?'0'+s:s;
    return h+':'+s;
}

setInterval(function () {
    var video = document.querySelector("video")
    var duration = $('#duration').attr("name")
    document.querySelector(".progress-bar").style.width = video.currentTime/duration * 100+"%";
    if (video.paused==true){
        var ispause="&#9658;"
    }else {
        var ispause ="II"
    }
    playBtn.innerHTML=ispause
    document.getElementById("time").innerHTML = timeTransformation(video.currentTime.toFixed(0)) + '/' + timeTransformation(duration)
},500)

document.querySelector(".progress").addEventListener('click', function(e){
    var video = document.querySelector("video")
    var offsetX = e.clientX - document.querySelector(".progress").clientLeft
    var left = $(".progress").offset().left
    video.currentTime = video.duration * ((offsetX - left)/$(".progress").width())
    video.play()
})
document.querySelector("#volume .progress").addEventListener('click', function(e){
    var offsetX = e.clientX - document.querySelector("#volume .progress").clientLeft
    var left = $("#volume .progress").offset().left
    $("#volume .progress-bar").width(offsetX - left);
    video.volume = $("#volume .progress-bar").width()/$("#volume .progress").width()
})

function videoStatus(){
    if(video.paused==true){
        video.play()
    }else{
        video.pause()
    };
};
playBtn.onclick=function(){
    videoStatus()
}
document.querySelector("video").onclick=function(){
    videoStatus()
}

document.onkeydown=function(event){
    var Ele = $('input:focus,textarea:focus')
    if (Ele.length != 0){
        return
    }
    event.preventDefault()
    var video = document.querySelector("video")
    var e=event || window.event || argument.callee.caller.arguments(0);
    if (e && e.keyCode==37){
        video.currentTime=video.currentTime - 5
    }else if (e && e.keyCode==39){
        video.currentTime=video.currentTime + 5
    }else if (e && e.keyCode==38){
        if (video.volume > 0.9){
            video.volume = 1
        }else{
            video.volume += 0.1
        }
        $("#volume .progress-bar").width($("#volume .progress").width() * video.volume);
    }else if (e && e.keyCode==40){
        if (video.volume < 0.1){
            video.volume = 0
        }else{
            video.volume -= 0.1
        }
    $("#volume .progress-bar").width($("#volume .progress").width() * video.volume);
    }
}

velocity.addEventListener('click',function(){
    if(video.playbackRate=="1.0"){
        video.playbackRate="1.5"
    }else if(video.playbackRate=="1.5"){
        video.playbackRate="2.0"
    }else if(video.playbackRate=="2.0"){
        video.playbackRate="1.0"
    };
    video.play()
    velocity.innerHTML=video.playbackRate.toFixed(1)
});

document.getElementById("minvideo").addEventListener('click',function(){
    video.requestPictureInPicture();
});

fullBtn.onclick = function(){
    fullscreen();
};
window.onresize = function(){
    var fullScreenEle = document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement;
    if(!fullScreenEle){
        fullBtn.setAttribute('class', 'glyphicon glyphicon-resize-full')
        fullBtn.onclick = function(){
            fullscreen();
        };
    }else if(fullScreenEle){
        fullBtn.setAttribute('class', 'glyphicon glyphicon-resize-small')
        fullBtn.onclick = function(){
            exitFullscreen();
        };
    };
    controlSize()
};
function fullscreen(){
    var element = document.querySelector('.video-grid');
    var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || element.mozRequestFullScreen || element.msRequestFullScreen;
    if (requestMethod){
        requestMethod.call(element)
    }else{
        return false
    }
}
function exitFullscreen(){
    var exitMethod = document.exitFullScreen || document.mozCancelFullScreen || document.webkitCancelFullScreen || document.msExitFullScreen;
    if (exitMethod){
        exitMethod.call(document)
    }else{
        return false
    }
}

$(window).scroll(function(){
    var scrollTop = $(this).scrollTop();
    var scrollHeight = $(document).height();
    var windowHeight = $(this).height();
    if(scrollTop + windowHeight >= scrollHeight){
        commentlist()
    }
});

document.getElementById('next').addEventListener('click',function (){
    single_playlist(3,3)
})
document.getElementById('last').addEventListener('click',function (){
    single_playlist(0,-3)
})

function videoRemain(){
    var videoList = document.querySelectorAll('.single-right-grids a');
    for(var i=0;i < videoList.length;i++){
        videoList[i].addEventListener('click', videoPlay.bind(videoList[i],videoList[i]),false);
    }
}

function commentSend(e){
    e.preventDefault()
    var user_id = getCookie("user_id")
    if(!user_id){
        myalert('Please login')
        return false
    }else if(!($("#comment-form textarea").val())){
        myalert('please input content')
        return false
    }else{
        var video_id = document.querySelector("video").getAttribute("name")
        var postData = $.param({'video_id': video_id}) + '&' + $.param({'content': $("#comment-form textarea").val()});
        $.ajax({
            url: '/comment/?video_id=' + video_id,
            type: 'POST',
            dataType: 'json',
            data: postData,
            success: function(res) {
                if(res.status==="success"){
                    myalert('Send success')
                    $("#comment-form textarea").val('')
                }else{
                    myalert('Send error, please try again')
                }
            }
        })
    }
}

function commentlist(){
    var video_id = document.querySelector("video").getAttribute("name")
    var start = document.querySelector(".media-grids").getAttribute("start")
    $.ajax({
        url: '/comment/?video_id=' + video_id + '&start=' + start + '&count=3',
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            if(res.status==="success"){
                if(res.data.length > 0){
                    document.querySelector(".media-grids").setAttribute("start",parseInt(start)+parseInt(res.data.length))
                    for (var i = 0; i <res.data.length ; i++) {
                        var data=res.data[i];
                        $('.media-grids').append(
                        '<div class="media">'
                        +'<h5>' + data.uname + '</h5>'
                        +'<div class="media-left">'
                        +'<a href="#">'
                        +'</a>'
                        +'</div>'
                        +'<div class="media-body">'
                        +'<p>' + data.content + '</p>'
                        +'</div>'
                        +'</div>'
                        )
                    }
                }
            }else{
                console.log(res.status);
            }
        }
    });
}

function single_playlist(cc,count) {
    var element = document.querySelector(".single-grid-right")
    var start = element.getAttribute("start")
    var classify = element.getAttribute('classify')
    if (start==0 && cc==count){
        start=cc
    }
    $.ajax({
        url: '/video/list/?listname=' + classify + '&start=' + start + '&count=' + count,
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            if(res.status==="success"){
                if(res.data.length > 0){
                    if (parseInt(count)>0 && res.data.length == parseInt(count)){
                        start = parseInt(start)+parseInt(count)
                    }else if (parseInt(count)>0 && res.data.length < parseInt(count)) {
                        start = parseInt(start)
                    }else if(parseInt(start)-res.data.length<0){
                        start = 0
                    }else {
                        start = parseInt(start)-res.data.length
                    }
                    element.setAttribute("start",start)
                    $('.single-grid-right .single-right-grids').remove()
                    for (var i = 0; i < res.data.length ; i++) {
                        var data=res.data[res.data.length-i-1];
                        $('.single-grid-right').prepend(
                            '<div class="single-right-grids">'
                            +'	<div class="col-md-8 single-right-grid-left">'
                            +'		<a href=" '+ data.url +' "><img src="' + data.img + '" alt="" /></a>'
                            +'	</div>'
                            +'	<div class="col-md-4 single-right-grid-right">'
                            +'		<a href="" class="title"> ' + data.title + '</a>'
                            +'		<p class="author"><a href="#" class="author">' + data.uname + '</a></p>'
                            +'	</div>'
                            +'	<div class="clearfix"> </div>'
                            +'</div>'
                        )
                    }
                }
                videoRemain()
            }else{
                console.log(res.status);
            }
        }
    });
}

function videoPlay(btn,e) {
    e.preventDefault()
    var url = btn.getAttribute('href')
    var video = document.querySelector("video")
    $.ajax({
        url:url,
        type:'GET',
        dataType:'json',
        success:function(res) {
            if(res.status == "error"){
                myalert(res.error)
            }else if(res.status=='success'){
                video.setAttribute('src',res.data['addr'])
                video.setAttribute('poster',res.data['img'])
                $(".media-grids").empty()
                $(".media-grids").attr("start",0)
                video.setAttribute('name',res.data["id"])
                $('#duration').attr("name",res.data['duration'])
                velocity.innerHTML=video.playbackRate.toFixed(1) + 'X'
                document.getElementById("comment_count").innerHTML='ALL Comments (' + res.data['comment_count'] + ')'
                videoInit()
            }
        },
    })
    return video;
}

window.onload=html_top(), single_playlist(0,3), userInfo(), setTimeout(function(){hideMask('#mask')},2000)
document.getElementById('identifying_code').addEventListener('click',identifying_code_click)
document.getElementById("signup_0_0").addEventListener('click',signup_00)
document.getElementById("signup_2_0").addEventListener('click',signup_20)
document.getElementById("comment-submit").addEventListener('click',commentSend)
