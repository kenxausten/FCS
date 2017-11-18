#coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''
from concurrent.futures import ThreadPoolExecutor
import shelve
from facepp import API, File
from itertools import chain
import platform
import logging
import os
import time

RASPBERRYPI = 'arm' in platform.platform().lower()
MAX_WORKERS = 5
SHELVE_DB = './face.db'
CONFIDENCE = 50

API_KEY = 'wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH'
API_SECRET = 'wff5ht9ky77pWK52a_NtwY3Csz47CSqT'

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

class FaceTask(object):

    def __init__(self, dbpath=SHELVE_DB):
        self.sdb = shelve.open(SHELVE_DB)
        if 'faces' not in self.sdb.keys():
            self.sdb['faces'] = {}
        self.api = API(API_KEY, API_SECRET)

    def detect(self):
        pass

    def get_facesets(self):
        """获取所有的faceset"""
        facesets = []
        for faceset in self.api.faceset.getfacesets()['facesets']:
            facesets.append(faceset['outer_id'])
        return facesets

    def get_faces(self, outer_id):
        """获取指定faceset中的face."""
        faces = []
        try:
            detail = self.api.faceset.getdetail(outer_id = outer_id)
            faces_tokens = detail['face_tokens']
        except ValueError:
            print(detail)
            faces_tokens = []

        for face_token  in faces_tokens:
            if face_token not in self.sdb['faces'].keys():
                faces.append(face_token)
            else:
                faces.append(self.db['faces'][face_token])
        return faces

    def upload_faces(self, outer_id, **kwargs):
        """上传face到指定的faceset
            keyword args  image_file or  image_url
        """
        name = kwargs.pop('name', None)
        if name == None:
            name = input('Please enter the picture name:')

        ret = self.api.detect(**kwargs)
        try:
            face_token = ret["faces"][0]["face_token"]
        except ValueError as e:
            logging.exception(str())
            return None
        self.sdb['faces'][face_token] = name
        self.sdb.sync()
        self.api.faceset.addface(outer_id=outer_id, face_tokens=face_token)
        return face_token

    def search_faces(self, outer_id, face_token):
        """ 根据face_token在指定的faceset中进行匹配搜索
        """
        search_result = self.api.search(face_token=face_token, outer_id=outer_id)
        try:
            results = search_result['results']
        except ValueError:
            print(search_result)
            results = []
        for face in results:
            if face['face_token'] in self.sdb['faces'].keys() and face['confidence'] > CONFIDENCE:
                return self.sdb['faces'][face['face_token']], face['face_token']
        return ''

    def show_load_face_name(self):
        return self.sdb['faces']

    def search_people_from_camera(self, outer_id):
        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg'%time.time()
        cmd = 'sudo raspistill -t 2000 -o %s' % image_name
        os.system(cmd)
        ret = self.detect(image_file=File(image_name))
        face_token=ret["faces"][0]["face_token"]

        return self.search_faces(outer_id, face_token)

    def update_faces_from_camera(self, outer_id):
        if not RASPBERRYPI:
            return None
        image_name = '%s.jpg'%time.time()
        cmd = 'sudo raspistill -t 2000 -o %s' % image_name
        os.system(cmd)
        return self.upload_faces(outer_id, image_file=File(image_name))


if __name__ == '__main__':
    face_task = FaceTask()
    sets = face_task.show_facesets()
    print(sets)
    if len(sets):
        face_task.get_faces(outer_id=sets[0])



