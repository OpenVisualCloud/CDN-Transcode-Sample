"use strict";

var videogrid = document.querySelector(".video-grid")
var video = document.querySelector("video")

var velocity = document.getElementById("velocity")
var formatChoose=document.querySelector('#format>div')
var formats=document.querySelectorAll('#format div button')

window.onload=userInfo(),html_top(),document.getElementById('identifying_code').addEventListener('click',identifying_code_click),document.getElementById("signup_0_0").addEventListener('click',signup_00),document.getElementById("signup_2_0").addEventListener('click',signup_20), setTimeout(function(){hideMask('#mask')},1000)

