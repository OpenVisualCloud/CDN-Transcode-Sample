import os
import shutil
from tornado.web import RequestHandler
from tasks import in_out

class UploadHandler(RequestHandler):
    def post(self, *args, **kwargs):
        fileName = self.get_body_argument('fileName', None)
        file = self.request.files.get('file', None)
        uploadStatus = self.get_body_argument('uploadStatus', None)
        timeStamp = self.get_body_argument('timeStamp', None)
        count = self.get_body_argument('count', None)
        from main import tempPath,srcPath
        fileName = timeStamp + "-" + fileName
        proPath = os.path.join(tempPath, fileName)
        if not os.path.isdir(proPath):
             os.makedirs(proPath)
        try:
            with open(os.path.join(proPath, count), 'wb') as f:
                f.write(file[0]['body'])
                self.set_status(200)
            if uploadStatus == 'end':
                res = in_out.delay(proPath, srcPath, fileName, count)	
        except Exception as e:
            self.set_status(401)
            print(e)
