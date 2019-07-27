"use strict";

var videogrid = document.querySelector(".video-grid")
var video = document.querySelector("video")
var velocity = document.getElementById("velocity")
var formatChoose=document.querySelector('#format>div')
var formats=document.querySelectorAll('#format div button')

$("#upload_form .input_file").change(
    function() {
        var filePath = $("#upload_form .input_file").val()
        var pos=filePath.lastIndexOf("\\");
        var fileName = filePath.substring(pos+1);
        $('#upload_form #title input').val(fileName)
    }
)

$("#upload_form").submit(function(){
    var user_id = getCookie("user_id")
    if(!user_id){
        myalert('Please login')
        return false
    }else if(!(document.querySelectorAll('#upload_form input')[0].files[0].name.endsWith('.mp4'))){
        myalert('muat be mp4 file')
        return false
    }else if(!$('#upload_form #title input').val().endsWith('.mp4')) {
        myalert('name must end of .mp4')
    }else{
        upload()
    }
});

function upload(){
    var timeStamp = new Date().getTime();
    const LENGTH = 1024 * 1024 * 10;
    var file = document.querySelectorAll('#upload_form input')[0].files[0];
    var fileName = $('#upload_form #title input').val();
    var totalSize = file.size;
    var start = 0;
    var end = start + LENGTH;
    var fd = null;
    var blob = null;
    var xhr = null;
    var sum = Math.ceil(totalSize/LENGTH)
    var count = 0
    var timer = setInterval(function () {
        if (start < totalSize) {
            fd = new FormData();
            xhr = new XMLHttpRequest();
            xhr.open('POST','/user/upload/',false);
            blob = file.slice(start, end);
            fd.append('timeStamp', timeStamp);
            fd.append('count', String(count));
            if (end >= totalSize){
                fd.append('uploadStatus', 'end')
            }
            fd.append('file', blob);
            fd.append('fileName', fileName);
            xhr.send(fd);
            if (xhr.readyState == 4 && xhr.status != 200){
                clearInterval(timer);
                var res = xhr.responseText
                var split1 = res.split('"error"')
                var split2 = split1[1].split('"status"')
                var split3 = split2[0].split('"')
                var split4 = split3[1].split('"')[0]
                myalert(split4)
                return false
            }
            start = end;
            end = start + LENGTH;
            count += 1;
            $('#submit input').val('upload ' + parseInt(count * 100 / sum) + "%")
        }else{
            $('#submit input').val('Submit')
            clearInterval(timer);
            myalert('upload access')
	}
    },100)
}
		
window.onload = userInfo(),html_top(), document.getElementById('identifying_code').addEventListener('click',identifying_code_click),document.getElementById("signup_2_0").addEventListener('click',signup_20),document.getElementById("signup_0_0").addEventListener('click',signup_00), setTimeout(function(){hideMask('#mask')},1000)

