import json
import os
import setting
from random import random
from tornado.web import RequestHandler
import random

from model.ser import user_ser
from model.user import User, Video
from setting import session, cursor, datetime
from tasks import in_out

def auth_login_json(func):
    def inner(self, *args, **kwargs):
        self.user_id = self.get_secure_cookie('user_id', None)
        try:
            self.user_id = int(bytes.decode(self.user_id))
            self.user = session.query(User).filter(User.id == self.user_id, User.is_delete == '0').first()
            session.close()
        except Exception as e:
            session.rollback()
            self.user = None
        if not self.user:
            res = {
                "error": "Please login",
                "status": "error",
            }
            self.set_status(206)
            self.write(json.dumps(res))
            return
        func(self, *args, **kwargs)
    return inner


class AuthcodeHandler(RequestHandler):
    def get(self):
        mobile = self.get_argument('mobile',None)
        try:
            user = session.query(User).filter(User.mobile==mobile).all()
            session.close()
        except Exception as e:
            session.rollback()
            raise e
        if user:
            res = {
                "error": "name was login up",
                "status": "error",
            }
            self.write(json.dumps(res))

        elif mobile:
            authcode = str(random.randrange(0, 10000))
            authcode = authcode.rjust(4, '0')
            print(authcode)
            cursor.set(mobile, authcode, ex=300,)
            res = {
                "status": "success",
            }
            self.set_secure_cookie('user_id','',expires_days=30)
            self.write(json.dumps(res))

    def post(self):
        mobile = self.get_argument('mobile',None)
        auth_code = self.get_argument('auth_code',None)
        name = self.get_argument('name',None)
        password=self.get_argument('password',None)
        authcode = cursor.get(mobile)
        try:
            user_name = session.query(User).filter(User.name == name).all()
            user_mobile = session.query(User).filter(User.mobile == mobile).all()
            if user_name:
                res = {
                    "error": "name was login up",
                    "status": "error",
                }
                self.write(json.dumps(res))
            elif user_mobile:
                res = {
                    "error": "phone was login up",
                    "status": "error",
                }
                self.write(json.dumps(res))
            elif authcode and auth_code==authcode.decode():
                user = User(name=name,password=password,mobile=mobile)
                session.add(user)
                session.commit()
                self.set_secure_cookie('user_id',str(user.id),expires_days=10)
                user_data = user_ser(user)
                session.close()
                res = {
                    "data": user_data,
                    "status": "success",
                }
                self.write(json.dumps(res))

            else:
                res = {
                    "error": "no code",
                    "status": "error",
                }
                self.write(json.dumps(res))

        except Exception as e:
            session.rollback()
            session.close()
            raise e
            res = {
                "error": "datebase error",
                "status": "error",
            }
            self.write(json.dumps(res))


class UploadHandler(RequestHandler):
    @auth_login_json
    def post(self, *args, **kwargs):
        fileName = self.get_body_argument('fileName', None)
        file = self.request.files.get('file', None)
        timeStamp = self.get_body_argument('timeStamp', None)
        uploadStatus = self.get_body_argument('uploadStatus', None)
        count = self.get_body_argument('count', None)
        cc = session.query(Video).filter(Video.title==fileName).first()
        session.close()
        from main import tempPath,srcPath
        proPath = os.path.join(tempPath, timeStamp + "-" + fileName)
        if cc:
            from tasks import del_file
            del_file(proPath)
            res = {
                "error": "File is exist, Please change name",
                "status": "error",
            }
            self.set_status(401)
            self.write(json.dumps(res))
            return
        if not os.path.isdir(proPath):
             os.makedirs(proPath)
        try:
            with open(os.path.join(proPath, count), 'wb') as f:
                f.write(file[0]['body'])
                self.set_status(200)
            if uploadStatus == 'end':
                res = in_out.delay(proPath, srcPath, fileName, count, self.user_id)
        except Exception as e:
            self.set_status(401)
            print(e)

class UserInfoHandler(RequestHandler):
    @auth_login_json
    def get(self):
        user_data = user_ser(self.user)
        res = {
            "data":user_data,
            "status": "success",
        }
        self.write(json.dumps(res))

    def post(self):
        mobile = self.get_argument("mobile")
        password = self.get_argument("password")
        try:
            user = session.query(User).filter(User.mobile == mobile).first()
            session.close()
            user_password = user.password
            if not user:
                res = {
                    "error": "user name is error",
                    "status": "error",
                }
                self.write(json.dumps(res))

            elif password == user_password:
                self.set_secure_cookie("user_id",str(user.id), expires_days=30)
                res = {
                    "status": "success",
                }
                self.write(json.dumps(res))
                return

            else:
                res = {
                    "error": "password error",
                    "status": "error",
                }
                self.write(json.dumps(res))

        except Exception as e:
            session.rollback()
            raise e
            res = {
                "error": "datebase",
                "status": "error",
            }
            self.write(json.dumps(res))
