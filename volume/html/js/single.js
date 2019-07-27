"use strict";

var videogrid = document.querySelector(".video-grid")
var video = document.querySelector("video")
var fullBtn = document.getElementById("maxvideo")
var playBtn=document.getElementById("pause")
var velocity = document.getElementById("velocity")
var duration = $('#duration').attr("name")

var controlSize = function(){
    setTimeout(function(){var height = $('.video-grid-video').outerHeight()
        $('.control').css('marginTop',-height*15/100);
        $('.control').css('height',height*10/100);
    },500)
}

$(window).resize(function(){
    controlSize()
})

videogrid.onmouseenter = function (){
    $(".control").slideDown(200)
};
videogrid.onmouseleave = function (){
    $(".control").slideUp(200)
};

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
    document.querySelector(".progress-bar").style.width = video.currentTime/duration * 100+"%";
    if (video.paused==true){
        var ispause="&nbsp;&Delta;&nbsp;&nbsp;"
    }else {
        var ispause ="&nbsp;ll&nbsp;&nbsp;"
    }
    playBtn.innerHTML=ispause
    document.getElementById("time").innerHTML = timeTransformation(video.currentTime.toFixed(0)) + '/' + timeTransformation(duration)
},500)

document.querySelector(".progress").addEventListener('click', function(e){
    var offsetX = e.clientX - document.querySelector(".progress").clientLeft
    var left = $(".progress").offset().left
    video.currentTime = video.duration * ((offsetX - left)/$(".progress").width())
    video.play()
})

playBtn.addEventListener('click', function(){
    if(video.paused==true){
        video.play()
    }else{
         video.pause()
         };
});

velocity.addEventListener('click',function(){
    if(video.playbackRate=="1.0"){
        video.playbackRate="1.5"
    }else if(video.playbackRate=="1.5"){
        video.playbackRate="2.0"
    }else if(video.playbackRate=="2.0"){
        video.playbackRate="1.0"
    };
    video.play()
    velocity.innerHTML=video.playbackRate.toFixed(1) + 'X'
});

document.getElementById("minvideo").addEventListener('click',function(){
    video.requestPictureInPicture();
});

fullBtn.addEventListener('click',fullscreen);

function fullscreen(){
    var elem =  document.querySelector('.video-grid');
    if(elem.webkitRequestFullScreen){
        elem.webkitRequestFullScreen();
    }else if(elem.mozRequestFullScreen){
        elem.mozRequestFullScreen();
    }else if(elem.requestFullScreen){
        elem.requestFullScreen();
    }else{
    
    }
   // fullBtn.removeEventListener('click', fullscreen)
   // fullBtn.addEventListener('click', exitFullscreen)
}

function exitFullscreen(){
    var elem =  document.querySelector('.video-grid');
    if(elem.webkitCancelFullScreen){
        elem.webkitCancelFullScreen();
    }else if(elem.mozCancelFullScreen){
        elem.mozCancelFullScreen();
    }else if(elem.cancelFullScreen){
        elem.cancelFullScreen();
    }else if(elem.msExitFullScreen){
        elem.msExitFullScreen();
    }else{
    
    }
    fullBtn.removeEventListener('click',exitFullscreen)
    fullBtn.addEventListener('click', fullscreen)
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
                    myalert('send')
                    $("#comment-form textarea").val('')
                }else{
                    myalert('send error')
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
            videoInit()
            }
        },
    })
}

window.onload=html_top(), single_playlist(0,3), userInfo(), setTimeout(function(){hideMask('#mask'),controlSize()},1000)
document.getElementById('identifying_code').addEventListener('click',identifying_code_click)
document.getElementById("signup_0_0").addEventListener('click',signup_00)
document.getElementById("signup_2_0").addEventListener('click',signup_20)
document.getElementById("comment-submit").addEventListener('click',commentSend)
