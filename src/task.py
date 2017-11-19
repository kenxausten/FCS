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
            GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 1)
        try:
            self.api.faceset.create(outer_id = 'default')
        except APIError as e:
            """如果 'default' 已创建， 忽略改错误。"""
            pass
        self.camera_lock = threading.Lock()

    def delete_faceset(self, outer_id):
        return self.api.faceset.delete(outer_id=outer_id, check_empty=0)

    def get_facesets(self):
        """获取所有的faceset"""
        try:
            facesets = self.api.faceset.getfacesets()['facesets']
        except KeyError:
            return None

        return [faceset['outer_id'] for faceset in facesets]

    def get_faces(self, outer_id=None):
        """获取指定faceset中的face."""
        if not outer_id:
            outer_id='default'

        faces = []
        try:
            detail = self.api.faceset.getdetail(outer_id = outer_id)
            faces_tokens = detail['face_tokens']
        except ValueError:
            return None

        def get_faces_name(face_token):
            face_detail = self.api.face.getdetail(face_token = face_token)
            return face_detail.get('user_id', None)

        tmp_executor = ThreadPoolExecutor()
        return list(tmp_executor.map(get_faces_name, faces_tokens))

    def upload_faces(self, outer_id=None, **kwargs):
        """上传face到指定的faceset
            keyword args  image_file or  image_url
        """
        if not outer_id:
            outer_id = 'default'
        name = kwargs.pop('name', None)
        if name == None:
            name = input('Please enter the picture name:')
        try:
            face_token = self.api.detect(**kwargs)["faces"][0]["face_token"]
        except KeyError as e:
            return None
        self.api.faceset.addface(outer_id=outer_id, face_tokens=face_token)
        self.api.face.setuserid(face_token='1f394f938b722e97d406a517faa5ae95', user_id=name)
        return face_token, name

    def search_faces(self,  face_token, outer_id=None):
        """ 根据face_token在指定的faceset中进行匹配搜索
        """
        if not outer_id:
            outer_id = 'default'
        try:
            results = self.api.search(face_token=face_token, outer_id=outer_id)['results']
        except ValueError:
            return None

        return [face['user_id'] for face in results if face['confidence'] > CONFIDENCE]

    def search_people_from_camera(self, outer_id=None):
        if not outer_id:
            outer_id = 'default'
        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg'%time.time()
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 1)
        cmd = 'sudo raspistill -t 2000 -o %s' % image_name
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 0)
        with self.camera_lock:
            os.system(cmd)
        ret = self.detect(image_file=File(image_name))
        face_token=ret["faces"][0]["face_token"]

        return self.search_faces(outer_id, face_token)

    def update_faces_from_camera(self, outer_id=None):
        if not outer_id:
            outer_id = 'default'

        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg'%time.time()
        cmd = 'sudo raspistill -t 2000 -o %s' % image_name
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 1)
        with self.camera_lock:
            os.system(cmd)
        GPIO.output(BCM_PIN4_SHOW_TAKE_PHOTO, 0)
        return self.upload_faces(outer_id, image_file=File(image_name))

    def clear(self):
        if RASPBERRYPI:
            GPIO.cleanup()

if __name__ == '__main__':
    face_task = FaceTask()
    sets = face_task.get_facesets()
    print(sets)
    if len(sets):
        print(face_task.get_faces(outer_id=sets[1]))



