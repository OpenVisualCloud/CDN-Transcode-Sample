import os
import shutil
from tornado.web import RequestHandler

class UploadHandler(RequestHandler):
    def post(self, *args, **kwargs):
        fileName = self.get_body_argument('fileName', None)
        file = self.request.files.get('file', None)
        uploadStatus = self.get_body_argument('uploadStatus', None)
        timeStamp = self.get_body_argument('timeStamp', None)
        from main import tempPath,srcPath
        fileName = timeStamp + "-" + fileName
        proPath = os.path.join(tempPath, fileName)
        try:
            with open(proPath, 'ab') as f:
                f.write(file[0]['body'])
                self.set_status(200)
            if uploadStatus == 'end':
                shutil.move(proPath, srcPath)
                cmd = "ffmpeg -i " + srcPath + "/" + fileName + " -vf thumbnail,scale=640:360 -frames:v 1 -y " + srcPath + "/" + fileName + ".png"
                os.system(cmd)		
        except Exception as e:
            print(e)
        return
