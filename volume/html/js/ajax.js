"use strict";

function getCookie(name) {
    var cook = document.cookie.match("\\b"+name+"([^:]*)\\b")
    return cook ? cook[1] : undefined
}

function videoRemain(){
    var videoList = document.querySelectorAll('.single-right-grid-left a');
    for(i=0;i < videoList.length;i++){
        videoList[i].addEventListener('click', videoPlay.bind(videoList[i],videoList[i]),false);
    }
}

function commentlist(){
    var video_id = document.querySelector("video").getAttribute("name")
    var start = document.querySelector(".media-grids").getAttribute("start")
    $.ajax({
        url: '/comment/list/?video_id=' + video_id + '&start=' + start + '&count=1',
        url: "json/Animated.json",
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
                            +'<h5>' + 'lalla' + '</h5>'
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
                    console.log(res.status);
                }
            }
        }
    }
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
                            +'		<a href=" '+ data.url +' " class="title"> ' + data.title + '</a>'
                            +'		<p class="author"><a href="#" class="author">' + data.uname + '</a></p>'
                            +'		<p class="views">' + data.video_likes + '</p>'
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
                my(res.error)
            }else if(res.status=='success'){
                video.setAttribute('src',res.data['addr'])
                video.setAttribute('poster',res.data['img'])
            }
        },
        headers:{
            "jump":'remain'
        }
    })
}

$("#upload_form").submit(function(){
    var postData = new FormData(document.getElementById("upload_form"));
    var user_id = getCookie("user_id")
    if(!user_id){
        myalert('Please login')
        return false
    }else {
        $.ajax({
            url: '/user/upload/',
            type: 'POST',
            data: postData,
            processData:false,
            contentType:false,
            dataType: 'json',
            success:function(res) {
                if(res.status=='success'){
                    myalert('upload success')
                }else {
                    myalert(res.error)
                }
            },
        })
    }
});
