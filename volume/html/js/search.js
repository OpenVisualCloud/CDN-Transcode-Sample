"use strict";

var ura=window.location.protocol+"//"+window.location.hostname+":"+window.location.port;
var videogrid = document.querySelector(".video-grid")
var video = document.querySelector("video")
var velocity = document.getElementById("velocity")
var formatChoose=document.querySelector('#format>div')
var formats=document.querySelectorAll('#format div button')

var searchlist = function(){
    var search_word = document.querySelector('.navbar-right input').innerHTML
    if (!search_word){
        search_word = $('#search_word').text()
    }
    $.ajax({
        url: ura+'/video/list/',
        type: 'POST',
        data : {'html_name':'search','search_word':search_word},
        dataType: 'json',
        success: function(res) {
            if(res.status==="success"){
                $('.top-grids').empty()
                $('.top-grids').append(
                    '<div class="recommended-info">'
                    +'<h3>Search Videos</h3>'
                    +'</div>'
                    +'<div class="clearfix"> </div>'
                )
                if(res.data.length > 0){
                    $('.top-grids').append(
                        '<div class="recommended-info hls_videos">'
                        +'<h4>HLS Videos</h4>'
                        +'</div>'
                    )
                    $('.top-grids').append(
                        '<div class="clearfix"> </div>'
                        +'<div class="recommended-info dash_videos">'
                        +'<h4>DASH Videos</h4>'
                        +'</div>'
                    )
                    for (var i = 0; i <res.data.length ; i++) {
                        var data=res.data[i];
                        if (data.classify == "hls"){
                            $('.hls_videos').append(
                                '<div class="col-md-3 resent-grid recommended-grid slider-top-grids" style="margin:1vw auto">' +
                                '<div class="resent-grid-img recommended-grid-img">'+
                                '	<a href="' + data.url + '"><img src="' + data.img + '" alt="" /></a>'+
                                '	<div class="time">' +
                                '		<p>' + data.create_time + '</p>' +
                                '	</div>' +
                                '	<div class="clck">' +
                                '		<span class="glyphicon glyphicon-time" aria-hidden="true"></span>' +
                                '	</div>' +
                                '</div>' +
                                '<div class="resent-grid-info recommended-grid-info">' +
                                '	<h4><a href="' + data.url + '" class="title title-info">' + data.title + '</a></h4>' +
                                '	<ul>' +
                                '		<li><p class="author author-info"><a href="#" class="author">' + data.uname + '</a></p></li>' +
                                '	</ul>' +
                                '</div>' +
                                '</div>'
                            );
                        }else if (data.classify == "dash"){
                            $('.dash_videos').append(
                                '<div class="col-md-3 resent-grid recommended-grid slider-top-grids" style="margin:1vw auto">' +
                                '<div class="resent-grid-img recommended-grid-img">'+
                                '       <a href="' + data.url + '"><img src="' + data.img + '" alt="" /></a>'+
                                '       <div class="time">' +
                                '               <p>' + data.create_time + '</p>' +
                                '       </div>' +
                                '       <div class="clck">' +
                                '               <span class="glyphicon glyphicon-time" aria-hidden="true"></span>' +
                                '       </div>' +
                                '</div>' +
                                '<div class="resent-grid-info recommended-grid-info">' +
                                '       <h4><a href="' + data.url + '" class="title title-info">' + data.title + '</a></h4>' +
                                '       <ul>' +
                                '               <li><p class="author author-info"><a href="#" class="author">' + data.uname + '</a></p></li>' +
                                '       </ul>' +
                                '</div>' +
                                '</div>'
                            );
                        }
                    }
                }
                else{
                    $('.top-grids').append(
                    '<div class="col-md-4 resent-grid recommended-grid slider-top-grids"><h5>Sorry, no relevant video was found. </h5></div>')
                };
            }else{
                console.log(res.status);
            }
        }
    });
}

$(".navbar-right").attr("onsubmit","return false")

window.onload = html_top(),searchlist(),userInfo(),document.getElementsByClassName("navbar-right")[0].addEventListener('click',searchlist),document.getElementById('identifying_code').addEventListener('click',identifying_code_click),document.getElementById("signup_2_0").addEventListener('click',signup_20),document.getElementById("signup_0_0").addEventListener('click',signup_00),hideMask("mask"), setTimeout(function(){hideMask('#mask')},1000)
