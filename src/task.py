#coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''

from concurrent.futures import ThreadPoolExecutor
import shelve
from facepp import API, File, APIError
from itertools import chain
import logging
import os
import time
import platform
import threading

RASPBERRYPI = 'arm' in platform.platform().lower()
if RASPBERRYPI:
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        print('Please install RPI.GPIO.')
        raise
else:
    GPIO = None


MAX_WORKERS = 5
SHELVE_DB = './face.db'
CONFIDENCE = 50

BCM_PIN4_SHOW_TAKE_PHOTO = 4

API_KEY = 'wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH'
API_SECRET = 'wff5ht9ky77pWK52a_NtwY3Csz47CSqT'

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

class FaceTask(object):

    def __init__(self, dbpath=SHELVE_DB):
        self.api = API(API_KEY, API_SECRET)
        if RASPBERRYPI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BCM_PIN4_SHOW_TAKE_PHOTO, GPIO.OUT)
            GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, True)
        try:
            self.api.faceset.create(outer_id = 'default')
        except APIError as e:
            """如果 'default' 已创建， 忽略改错误。"""
            pass
        self.camera_lock = threading.Lock()

    def delete_faceset(self, outer_id):
        try:
            return self.api.faceset.delete(outer_id=outer_id, check_empty=0)
        except APIError as e:
            return str(e)

    def add_faceset(self, outer_id):
        try:
            return self.api.faceset.create(outer_id=outer_id)
        except APIError as e:
            return str(e)

    def get_facesets(self):
        """获取所有的faceset"""
        try:
            facesets = self.api.faceset.getfacesets()['facesets']
        except KeyError:
            return None

        return [faceset['outer_id'] for faceset in facesets]

    def get_faceset(self, outer_id='default'):
        """获取指定faceset中的face."""
        faces = []
        try:
            detail = self.api.faceset.getdetail(outer_id = outer_id)
            faces_tokens = detail['face_tokens']
        except ValueError:
            return None
        except APIError:
            return None

        def get_faces_name(face_token):
            face_detail = self.api.face.getdetail(face_token = face_token)
            return face_detail.get('user_id', None)

        tmp_executor = ThreadPoolExecutor()
        return list(tmp_executor.map(get_faces_name, faces_tokens))

    def upload_faces(self, outer_id='default', **kwargs):
        """上传face到指定的faceset
            keyword args  image_file or  image_url
        """
        name = kwargs.pop('name', None)
        if name == None:
            name = raw_input('Please enter the picture name:')
        try:
            face_token = self.api.detect(**kwargs)["faces"][0]["face_token"]
        except (KeyError, IndexError): 
            return None
        self.api.faceset.addface(outer_id=outer_id, face_tokens=face_token)
        self.api.face.setuserid(face_token=face_token, user_id=name)
        
        img = db.models.Image(name=name, path=kwargs.pop('image_path'), token=face_token)
        img.save()
        
        return face_token, name

    def search_faces(self,  face_token, outer_id='default'):
        """ 根据face_token在指定的faceset中进行匹配搜索
        """
        try:
            results = self.api.search(face_token=face_token, outer_id=outer_id)['results']
        except (KeyError):
            return None

        return [face['user_id'] for face in results if face['confidence'] > CONFIDENCE]

    def search_people_from_camera(self, outer_id='default'):
        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg' % time.time()
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 1)
        cmd = 'sudo raspistill -t 2000 -o %s -p 100,100,300,200 -q 5' % image_name
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 0)
        with self.camera_lock:
            os.system(cmd)
        ret = self.api.detect(image_file=File(image_name))
        
        try:
            face_token=ret["faces"][0]["face_token"]
        except (IndexError, KeyError):
            if isinstance(ret, dict) and ('error_message' in ret.keys()):
                return ret['error_message']
            return 'The picture is invalid.'

        return self.search_faces(face_token, outer_id=outer_id)

    def update_faces_from_camera(self, outer_id='default'):
        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg'%time.time()
        cmd = 'sudo raspistill -t 2000 -o %s -p 100,100,300,200 -q 5' % image_name
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, True)
        with self.camera_lock:
            os.system(cmd)
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, False)
        return self.upload_faces(outer_id, image_file=File(image_name), image_path=image_name)

    def clear(self):
        if RASPBERRYPI:
            GPIO.cleanup()

if __name__ == '__main__':
    face_task = FaceTask()
    sets = face_task.get_facesets()
    print(sets)
    if len(sets):
        print(face_task.get_faces(outer_id=sets[1]))