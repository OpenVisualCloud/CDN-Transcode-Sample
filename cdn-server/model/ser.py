from model.user import User
from setting import session

def comment_ser(obj):
    return {
        "id":obj.id,
        "content":obj.content,
        "create_time":"6789098",
        "uname":obj.c2u.name,
    }

def video_ser(obj, listname):
    comment_count=len(obj.v2c)
    uid=obj.uid
    if listname == 'hls':
        src = '/hls' + obj.addr + '/index.m3u8'
    elif listname == 'dash':
        src = '/dash' + obj.addr + '/index.mpd'
    return {
        "id":obj.id,
        "create_time":"2019 04 11",
        "img":obj.img,
        "title":obj.title,
        "uname":obj.v2u.name,
        "duration":obj.duration,
        "addr":src,
        "classify":listname,
        "url":"/video/play/?id="+str(obj.id) + "&listname=" + listname,
        "content":obj.content,
        "comment_count":comment_count,
    }

def user_ser(obj):
    return {
        'id':obj.id,
        'mobile':obj.mobile,
        'name':obj.name,
    }
