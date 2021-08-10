import os
import shutil
from time import sleep
from celery import Celery

def del_file(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    if os.path.exists(path):
        os.remove(path)

celery = Celery('tasks',
    broker = 'redis://redis-service:6379',
    brckend = 'redis://redis-service:6379')

@celery.task
def in_out(proPath, srcPath, fileName, count):
    i=0
    while i < 20:
        if len(os.listdir(proPath)) == int(count) + 1:
            try:
                with open(os.path.join(srcPath, fileName), "wb") as upload_file:
                    for i in range(0, int(count) + 1):
                        with open(os.path.join(proPath, str(i)), "rb") as data:
                            upload_file.write(data.read())
                cmd = "ffmpeg -i " + os.path.join(srcPath, fileName) + " -vf thumbnail,scale=640:360 -frames:v 1 -y " + srcPath + "/" + fileName + ".png"
                res = os.system(cmd)
                if not res == 0:
                    raise Exception("image error")
            except Exception as e:
                del_file(os.path.join(srcPath, fileName, '0'))
                del_file(os.path.join(srcPath, fileName))
                del_file(proPath)
                return (e)
            else:
                del_file(proPath)
                return ('delete success')
        else:
            sleep(1)
            i += 1
    return ("can't find file")
