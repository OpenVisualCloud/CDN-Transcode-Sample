import json
import re

from tornado.web import RequestHandler

from model.ser import video_ser
from model.user import Video, Comment, User
from setting import session


class PlaylistHandler(RequestHandler):
    def get(self, num):
        listname=self.get_argument("listname", None)
        start=int(self.get_argument("start", 0))
        count=int(self.get_argument("count", 4))
        if count < 0:
            count = -count
            start = start - count * 2
            if start < 0:
                start = 0
        try:
            videos = session.query(Video).filter(Video.is_delete=="0")[start:start+count]
            videos_data = []
            for i in videos:
                videos_data.append(video_ser(i, listname))
            res = {
                "data": videos_data,
                "status": "success",
                }
        except Exception as e:
            res = {
                "data": "data error",
                "status": "error",
                }
        session.rollback()
        session.close()
        
        self.write(json.dumps(res))

    def post(self, *args, **kwargs):
        html_name = self.get_argument("html_name",None)
        search_word = self.get_argument('search_word',None)

        if search_word and html_name=="search":
            try:
                videos = session.query(Video).filter(Video.title.like("%"+search_word+"%")).all()
            except Exception as e:
                session.rollback()
                raise e
            videos_data=[]
            listnames = ['hls', 'dash']
            for i in videos:
                for listname in listnames:
                    videos_data.append(video_ser(i, listname))
            session.close()
            res = {
                "data": videos_data,
                "status": "success",
            }
            self.write(json.dumps(res))
        else:
            self.render("/var/www/html/search.html", search_word=search_word)


class VideoHandler(RequestHandler):
    def get(self):
        listname=self.get_argument("listname", None)
        try:
            Referer = self.request.headers['Referer']
        except:
            Referer = "none_id"
        video_id = self.get_argument("id",None)
        try:
            video = session.query(Video).filter(Video.id == video_id, Video.is_delete == '0').first()
            video_data = video_ser(video, listname)
        except Exception as e:
            session.rollback()
            session.close()
        if re.search("id=", Referer) and video_id:
            res = {
                "data": video_data,
                "status": "success",
            }
            self.write(json.dumps(res))
        elif video_id:
            self.render("/var/www/html/single.html",video_data=video_data)
