import os
import shutil
from time import sleep
from celery import Celery
from model.user import User, Video
from setting import session, cursor, datetime



def del_file(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    if os.path.exists(path):
        os.remove(path)

celery = Celery('tasks',
    broker = 'redis://redis-service:6379',
    brckend = 'redis://redis-service:6379')

@celery.task
def in_out(proPath, srcPath, fileName, count, user_id):
    i=0
    while i < 10:
        i += 1
        if len(os.listdir(proPath)) == int(count) + 1:
            try:
                cmd = "ffmpeg -i " + os.path.join(proPath, '0') + " -vf thumbnail,scale=640:360 -frames:v 1 -y " + srcPath + "/" + fileName + ".png"
                res = os.system(cmd)
                upload_file = open(os.path.join(srcPath, fileName), "wb")
                for i in range(0, int(count) + 1):
                    with open(os.path.join(proPath, str(i)), "rb") as data:
                        upload_file.write(data.read())
                upload_file.close()
                cmd = 'ffprobe -i %s -show_entries format=duration -v quiet -of csv="p=0"' % os.path.join(srcPath, fileName)
                res = os.popen(cmd)
                video_info = res.read()
                duration = int(video_info.split('.')[0])
                if not os.path.exists(srcPath + "/" + fileName + ".png"):
                    sleep(5)
                if not os.path.exists(srcPath + "/" + fileName + ".png"):
                    raise Exception("image error")
            except Exception as e:
                del_file(os.path.join(srcPath, fileName, '0'))
                del_file(os.path.join(srcPath, fileName))
                del_file(proPath)
                session.close()
                return (e)
            else:
                video = Video(title=fileName, uid=user_id, addr="/" + fileName,duration = duration, img="/thumbnail/" + fileName + ".png")
                print(video)
                try:
                    session.add(video)
                    session.commit()
                except Exception as e:
                    session.rollback()

                session.close()
                del_file(proPath)
                return ('delete success')
        else:
            sleep(1)
    del_file(srcPath + "/" + fileName + ".png")
    del_file(proPath)
    return ("can't find file")
