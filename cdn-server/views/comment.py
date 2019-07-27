import json

# import render as render
from tornado.web import RequestHandler

from views.user import auth_login_json
from model.ser import video_ser, comment_ser
from model.user import Video, Comment
from setting import session


class CommentHandler(RequestHandler):
    def get(self):
        video_id=self.get_argument("video_id", None)
        start=int(self.get_argument("start", 0))
        count=int(self.get_argument("count", 5))
        try:
            print(session.query(Comment).filter(Video.id==video_id, Video.is_delete=="0").first())
            comments = session.query(Video).filter(Video.id==video_id, Video.is_delete=="0").first().v2c[start:start+count]
        except Exception as e:
            session.rollback()
            raise e
        comments_data = []
        for i in comments:
            comments_data.append(comment_ser(i))
        session.close()
        res = {
            "data": comments_data,
            "status": "success",
        }
        self.write(json.dumps(res))

    @auth_login_json
    def post(self):
        video_id= int(self.get_argument("video_id",None))
        content = self.get_argument('content', None)
        comment = Comment(uid = self.user_id, vid = video_id, content = content)
        try:
            session.add(comment)
            session.commit()
            res = {
                "status": "success",
            }
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
            res = {
                "status": "error",
            }
        self.write(json.dumps(res))
