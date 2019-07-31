"use strict";

function hideMask(id) {
    $(id).css('opacity','1');
}

document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        document.body.style.display = "block";
    }else {
        document.body.style.display = "none";
    };
};

var userInfo = function () {
    $.ajax({
        url: '/user/info/',
        type: 'GET',
        dataType: 'json',
        success:function(res) {
            if(res.status == "success"){
                document.getElementById("signin_0").innerText=res.data["name"]
                document.getElementById("signin_1").innerHTML='Sign Out'
                document.getElementById("signin_1").addEventListener("click",function(){
                    document.cookie = "user_id" + '=v;  expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/',
                    userInfo()
                })
            }else {
                document.getElementById("signin_0").innerText="Sign Up"
                document.getElementById("signin_1").innerHTML='Sign In'
            }
        }
    })
}

var html_top = function () {
    if (document.getElementById('mask')){
        var top = $('#mask')
    }else{
        var top = $('body')
    }
    top.prepend("    <nav class=\"navbar navbar-inverse navbar-fixed-top\">\n" +
        "      <div class=\"container-fluid\">\n" +
        "        <div class=\"navbar-header\">\n" +
        "          <button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">\n" +
        "            <span class=\"sr-only\">Toggle navigation</span>\n" +
        "            <span class=\"icon-bar\"></span>\n" +
        "            <span class=\"icon-bar\"></span>\n" +
        "            <span class=\"icon-bar\"></span>\n" +
        "          </button>\n" +
        "          <a class=\"navbar-brand\" href=\"/index.html\"><h1><img src=\"/images/logo.png\" alt=\"\" /></h1></a>\n" +
        "        </div>\n" +
        "        <div id=\"navbar\" class=\"navbar-collapse collapse\">\n" +
        "\t\t\t<div class=\"top-search\">\n" +
        "\t\t\t\t<form class=\"navbar-form navbar-right\" action=\"/video/list/\" method=\"post\">\n" +
        "\t\t\t\t\t<input type=\"text\" class=\"form-control\" placeholder=\"Search...\" name=\"search_word\">\n" +
        "\t\t\t\t\t<input type=\"submit\" value=\" \">\n" +
        "\t\t\t\t</form>\n" +
        "\t\t\t</div>\n" +
        "\t\t\t<div class=\"header-top-right\">\n" +
        "\t\t\t\t<div class=\"file\">\n" +
        "\t\t\t\t\t<a href=\"/upload.html\">Upload</a>\n" +
        "\t\t\t\t</div>\n" +
        "\t\t\t\t<div class=\"signin\" >\n" +
        "\t\t\t\t\t<a href=\"#small-dialog2\" class=\"play-icon popup-with-zoom-anim\" id=\"signin_0\">Sign Up</a>\n" +
        "\t\t\t\t\t<!-- pop-up-box -->\n" +
        "\t\t\t\t\t<script type=\"text/javascript\" src=\"/js/modernizr.custom.min.js\"></script>\n" +
        "<script>" +
        "\t\t$(document).ready(function() {\n" +
        "\t\t\t\t\t\t\t\t\t\t\t$('.popup-with-zoom-anim').magnificPopup({\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\ttype: 'inline',\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tfixedContentPos: false,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tfixedBgPos: true,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\toverflowY: 'auto',\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tcloseBtnInside: true,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tpreloader: false,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tmidClick: true,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tremovalDelay: 300,\n" +
        "\t\t\t\t\t\t\t\t\t\t\t\tmainClass: 'my-mfp-zoom-in'\n" +
        "\t\t\t\t\t\t\t\t\t\t\t});\n" +
        "\t\t\t\t\t\t\t\t\t\t\t});"+
        "</script>" +
        "\t\t\t\t\t<link href=\"/css/popuo-box.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" />\n" +
        "\t\t\t\t\t<!--//pop-up-box -->\n" +
        "\t\t\t\t\t<div id=\"small-dialog2\" class=\"mfp-hide\">\n" +
        "\t\t\t\t\t\t<h3>Create Account</h3>\n" +
        "\t\t\t\t\t\t<div class=\"social-sits\">\n" +
        "\t\t\t\t\t\t\t<!--<div class=\"facebook-button\">-->\n" +
        "\t\t\t\t\t\t\t\t<!--<a href=\"#\">Connect with XXX</a>-->\n" +
        "\t\t\t\t\t\t\t<!--</div>-->\n" +
        "\t\t\t\t\t\t\t<!--<div class=\"chrome-button\">-->\n" +
        "\t\t\t\t\t\t\t\t<!--<a href=\"#\">Connect with XXX</a>-->\n" +
        "\t\t\t\t\t\t\t<!--</div>-->\n" +
        "\t\t\t\t\t\t\t<div class=\"weixin-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"qq-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"button-bottom\">\n" +
        "\t\t\t\t\t\t\t\t<p>Already have an account? <a href=\"#small-dialog\" class=\"play-icon popup-with-zoom-anim\">Login</a></p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"signup\">\n" +
        "\t\t\t\t\t\t\t<form>\n" +
        "\t\t\t\t\t\t\t\t<input type=\"text\" id='mobile_0' class=\"mobile\" placeholder=\"Mobile Number\" required=\"required\" maxlength=\"11\" pattern=\"[1-9]{1}\\d{10}\" title=\"Enter a valid mobile number\" />\n" +
        "\t\t\t\t\t\t\t</form>\n" +
        "\t\t\t\t\t\t\t<div class=\"continue-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#small-dialog2\" target=\"_self\" class=\"hvr-shutter-out-horizontal play-icon popup-with-zoom-anim\" id=\"identifying_code\">Auth Code</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"clearfix\"> </div>\n" +
        "\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t<div id=\"small-dialog3\" class=\"mfp-hide\">\n" +
        "\t\t\t\t\t\t<h3>Create Account</h3>\n" +
        "\t\t\t\t\t\t<div class=\"social-sits\">\n" +
        "\t\t\t\t\t\t\t<div class=\"facebook-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"chrome-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"button-bottom\">\n" +
        "\t\t\t\t\t\t\t\t<p>Already have an account? <a href=\"#small-dialog\" class=\"play-icon popup-with-zoom-anim\">Login</a></p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"signup\">\n" +
        "\t\t\t\t\t\t\t<form id=\"signup_0\" onsubmit=\"return false;\">\n" +
        "\t\t\t\t\t\t\t\t<input type=\"text\" class=\"email\" placeholder=\"name\" title=\"Enter name\" name=\"name\" required=\"required\" maxlength=\"10\" pattern=\"\\w+\" />\n" +
        "\t\t\t\t\t\t\t\t<input type=\"password\" placeholder=\"Password\" title=\"Minimum 6 characters required\" autocomplete=\"off\" required=\"required\" name=\"password\" maxlength=\"20\" pattern=\"\\w{6,20}\"/>\n" +
        "\t\t\t\t\t\t\t\t<input type=\"text\" class=\"mobile\" placeholder=\"Verification Code\" title=\"Enter auth code\" name=\"auth_code\" required=\"required\" maxlength=\"4\" pattern=\"[0-9]{4}\" />\n" +
        "\t\t\t\t\t\t\t\t<input type=\"submit\"  value=\"Sign Up\" id=\"signup_0_0\" onsubmit=\"return false;\"/>\n" +
        "\t\t\t\t\t\t\t\t<!--<p><input type=\"BUTTON\" class=\"\" value=\"Sign Up\" id=\"login_in\"></p>-->\n" +
        "\t\t\t\t\t\t\t</form>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"clearfix\"> </div>\n" +
        "\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t<div id=\"small-dialog7\" class=\"mfp-hide\">\n" +
        "\t\t\t\t\t\t<h3>Create Account</h3>\n" +
        "\t\t\t\t\t\t<div class=\"social-sits\">\n" +
        "\t\t\t\t\t\t\t<div class=\"facebook-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"chrome-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"button-bottom\">\n" +
        "\t\t\t\t\t\t\t\t<p>Already have an account? <a href=\"#small-dialog\" class=\"play-icon popup-with-zoom-anim\" >Login</a></p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<!--<div class=\"signup\">-->\n" +
        "\t\t\t\t\t\t\t<!--<form action=\"upload.html\">-->\n" +
        "\t\t\t\t\t\t\t\t<!--<input type=\"text\" class=\"email\" placeholder=\"Email\" required=\"required\" pattern=\"([\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4})?\" title=\"Enter a valid email\"/>-->\n" +
        "\t\t\t\t\t\t\t\t<!--<input type=\"password\" placeholder=\"Password\" required=\"required\" pattern=\".{6,}\" title=\"Minimum 6 characters required\" autocomplete=\"off\" />-->\n" +
        "\t\t\t\t\t\t\t\t<!--<input type=\"submit\"  value=\"Sign In\"/>-->\n" +
        "\t\t\t\t\t\t\t<!--</form>-->\n" +
        "\t\t\t\t\t\t<!--</div>-->\n" +
        "\t\t\t\t\t\t<div class=\"clearfix\"> </div>\n" +
        "\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t<div id=\"small-dialog4\" class=\"mfp-hide\">\n" +
        "\t\t\t\t\t\t<h3>Feedback</h3>\n" +
        "\t\t\t\t\t\t<div class=\"feedback-grids\">\n" +
        "\t\t\t\t\t\t\t<div class=\"feedback-grid\">\n" +
        "\t\t\t\t\t\t\t\t<p>Suspendisse tristique magna ut urna pellentesque, ut egestas velit faucibus. Nullam mattis lectus ullamcorper dui dignissim, sit amet egestas orci ullamcorper.</p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"button-bottom\">\n" +
        "\t\t\t\t\t\t\t\t<p><a href=\"#small-dialog\" class=\"play-icon popup-with-zoom-anim\" >Sign in</a> to get started.</p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t</div>\n" +
        "\t\t\t\t</div>\n" +
        "\t\t\t\t<div class=\"signin\" >\n" +
        "\t\t\t\t\t<a href=\"#small-dialog\" class=\"play-icon popup-with-zoom-anim\" id=\"signin_1\" onsubmit=\"return false;\">Sign In</a>\n" +
        "\t\t\t\t\t<div id=\"small-dialog\" class=\"mfp-hide\">\n" +
        "\t\t\t\t\t\t<h3>Login</h3>\n" +
        "\t\t\t\t\t\t<div class=\"social-sits\">\n" +
        "\t\t\t\t\t\t\t<div class=\"facebook-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"chrome-button\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Connect with XXX</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t\t<div class=\"button-bottom\">\n" +
        "\t\t\t\t\t\t\t\t<p>New account? <a href=\"#small-dialog2\" class=\"play-icon popup-with-zoom-anim\">Signup</a></p>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"signup\" >\n" +
        "\t\t\t\t\t\t\t<!--<form id=\"signin_2\" onsubmit=\"return false;\" >-->\n" +
        "\t\t\t\t\t\t\t\t<form id=\"signup_2\" onsubmit=\"return false;\">\n" +
        "\t\t\t\t\t\t\t\t<input type=\"text\" class=\"email\" placeholder=\"Enter mobile\" name=\"mobile\" required=\"required\" pattern=\"[1][3,4,5,7,8][0-9]{9}\" maxlength=\"20\" title=\"Minimum mobile\"/>\n" +
        "\t\t\t\t\t\t\t\t<input type=\"password\" placeholder=\"Password\" required=\"required\" pattern=\"\\w{6,20}\" name=\"password\" title=\"Minimum 6 characters required(6-20)\" maxlength=\"20\" autocomplete=\"off\" />\n" +
        "\t\t\t\t\t\t\t\t<input type=\"submit\"  value=\"LOGIN\" id=\"signup_2_0\"/>\n" +
        "\t\t\t\t\t\t\t</form>\n" +
        "\t\t\t\t\t\t\t<div class=\"forgot\">\n" +
        "\t\t\t\t\t\t\t\t<a href=\"#\">Forgot password ?</a>\n" +
        "\t\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t</div>\n" +
        "\t\t\t\t\t\t<div class=\"clearfix\"> </div>\n" +
        "\t\t\t\t\t</div>\n" +
        "\t\t\t\t</div>\n" +
        "\t\t\t\t<div class=\"clearfix\"> </div>\n" +
        "\t\t\t</div>\n" +
        "        </div>\n" +
        "\t\t<div class=\"clearfix\"> </div>\n" +
        "      </div>\n" +
        "    </nav>")
}


function getCookie(name) {
    var cook = document.cookie.match("\\b"+name+"([^:]*)\\b")
    return cook ? cook[1] : undefined
}

function isPoneAvailable(str) {
    var mobile=/^[1][3,4,5,7,8][0-9]{9}$/;
    if (!mobile.test(str)) {
        return false;
    }else{
        return true;
    }
}

function isPassword(str) {
    var password=/^\w{6,20}$/;
    if (!password.test(str)) {
        return false;
    }else{
        return true;
    }
}

function iscode(str) {
    var code=/^\d{4}$/;
    if (!code.test(str)) {
        return false;
    } else {
        return true;
    }
}

function identifying_code_click() {
    var mobile = $('#mobile_0').val()
    if (isPoneAvailable(mobile)){
        get_authcode(mobile)
    }else {
        myalert('please check phone number')
        document.getElementById('identifying_code').setAttribute('href','#small-dialog2')
    }
}

function get_authcode(mobile) {
    $.ajax({
        url:'/user/sign_up/auth_code/?mobile=' + mobile,
        type:'GET',
        dataType:'json',
        success:function(res) {
            if(res.status == "error"){
                myalert(res.error)
            }else if(res.status=='success'){
                document.getElementById('identifying_code').setAttribute('href','#small-dialog3')
                document.getElementById('identifying_code').removeEventListener('click',identifying_code_click)
                $('#identifying_code').click();
                document.getElementById('identifying_code').setAttribute('href','#small-dialog2')
                document.getElementById('identifying_code').addEventListener('click',identifying_code_click)
            }
        },
    })
}

var signup_00 = function(){
    var mobile = $('#mobile_0').val()
    var postData = $.param({'mobile': mobile}) + '&' + $("#signup_0").serialize();
    if (!isPassword($('#signup_0').children().eq(1).val()) || !iscode($('#signup_0').children().eq(2).val())){
        return false
    }
    $.ajax({
        url: '/user/sign_up/auth_code/',
        type: 'POST',
        dataType: 'json',
        data: postData,
        success:function(res) {
            if(res.status == "error"){
                myalert(res.error)
            }else if(res.status=='success'){
                userInfo()
                $(".mfp-close").click()
            }
        },
    })
}

var signup_20 = function () {
    var postData = $("#signup_2").serialize();
    console.log($("#signup_2 input")[0])
    var mobile = $("#signup_2 input")[0].value
    var password = $("#signup_2 input")[1].value
    if(!isPoneAvailable(mobile) || !isPassword(password)){
        return false
    }
    $.ajax({
        url: '/user/info/',
        type: 'POST',
        data: postData,
        dataType: 'json',
        success:function(res) {
            if(res.status=='success'){
                userInfo()
                $(".mfp-close").click()
            }else {
                myalert(res.error)
            }
        },
    })
}

function myalert(str) {
    var div = '<div class="mark"><div></div></div>';
    $('body').append(div)
    $('.mark div').html(str);
    $('.mark').show();
    setTimeout(function() {
        $('.mark').hide();
        $('.mark').remove();
    }, 2000)
}
