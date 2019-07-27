"use strict";

var ura=window.location.protocol+"//"+window.location.hostname+":"+window.location.port;
var recommendedlist_name = document.querySelector('#recommended .recommended-info h3').innerHTML.toLowerCase()
var sportlist_name = document.querySelector('#sport .recommended-info h3').innerHTML.toLowerCase()

var recommendedlist = function(start,count){
    $.ajax({
        url: ura+'/video/list/?listname='+ recommendedlist_name +'&start=' + start + '&count=' + count,
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            if(res.status==="success"){
                if(res.data.length > 0){
                    $('#recommended').empty()
                    $('#recommended').append(
                        '<div class="recommended-info">'
                        +'<h3>'
                        +recommendedlist_name
                        +'</h3>'
                        +'</div>'
                    ) 
                    for (var i = 0; i <res.data.length ; i++) {
                        var data=res.data[i];
                      	$('#recommended').append(
                            '<div class="col-md-3 resent-grid recommended-grid">'
                            +'<div class="resent-grid-img recommended-grid-img">'
                            +'<a href="' + data.url + '"><img src="' + data.img + '" alt="" /></a>'
                            +'<div class="time small-time">'
                            +'<p>' + data.create_time + '</p>'
                            +'</div>'
                            +'<div class="clck small-clck">'
                            +'<span class="glyphicon glyphicon-time" aria-hidden="true"></span>'
                            +'</div>'
                            +'</div>'
                            +'<div class="resent-grid-info recommended-grid-info video-info-grid">'
                            +'<h5><a href="' + data.url + '" class="title">' + data.title + '</a></h5>'
                            +'<ul>'
                            +'<li><p class="author author-info"><a href="' + data.url + '" class="author">' + data.uname + '</a></p></li>'
                            +'</ul>'
                            +'</div>'
                            +'</div>'							
                        );
                    }
                    $('#recommended').append(
                        '<div class="clearfix"> </div>'
                    )
                }
            }else{
                console.log('error');
            }
        }
    });
}
recommendedlist(0,4)

var sportlist = function(start,count){
    $.ajax({
        url: ura+'/video/list/?listname='+ sportlist_name +'&start=' + start + '&count=' + count,
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            if(res.status==="success"){
                if(res.data.length > 0){
                    $('#sport').empty()	
                    $('#sport').append(
                        '<div class="recommended-info">'
                        +'<h3>'
                        +sportlist_name
                        +'</h3>'
                        +'</div>'
                    )				
                    for (var i = 0; i <res.data.length ; i++) {
                        var data=res.data[i];
                        $('#sport').append(
                            '<div class="col-md-3 resent-grid recommended-grid">'
                            +'<div class="resent-grid-img recommended-grid-img">'
                            +'<a href="' + data.url + '"><img src="' + data.img + '" alt="" /></a>'
                            +'<div class="time small-time">'
                            +'<p>' + data.create_time + '</p>'
                            +'</div>'
                            +'<div class="clck small-clck">'
                            +'<span class="glyphicon glyphicon-time" aria-hidden="true"></span>'
                            +'</div>'
                            +'</div>'
                            +'<div class="resent-grid-info recommended-grid-info video-info-grid">'
                            +'<h5><a href="' + data.url + '" class="title">' + data.title + '</a></h5>'
                            +'<ul>'
                            +'<li><p class="author author-info"><a href="' + data.authorurl + '" class="author">' + data.uname + '</a></p></li>'
                            +'</ul>'
                            +'</div>'
                            +'</div>'								
                        );
                    }
                    $('#sport').append('<div class="clearfix"> </div>')
                }
            }else{
                console.log('error');
            }
        }
    });
}
sportlist(0,4)
