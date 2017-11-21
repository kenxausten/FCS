#! /usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Created on 2017/11/16

@author: Fucheng Xu
'''

from facepp.face import *

class FCS(object):
    def __init__(self, faceset_name):
        self.face_service = FaceService(api_key='wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH', api_secret='wff5ht9ky77pWK52a_NtwY3Csz47CSqT')
        self.faceset_name = faceset_name
        
    def init_raw_images(self, image_path, image_count):
        result = self.face_service.set_create(self.faceset_name)
        token_file_name = {}
        
        for image_index in range(1, image_count+1):
            file_path = '%s/%d.jpg' % (image_path, image_index)
            token_id = self.face_service.get_img_token(file_path)
            if token_id:
                result = self.face_service.set_add(self.faceset_name, token_id)
                token_file_name[token_id] = file_path
        
        return token_file_name
    
if __name__ == '__main__':
    raw_image_path = './image/raw_image/'
    raw_image_count = 5
    
    fcs =  FCS(faceset_name='yy')
    print fcs.init_raw_images(raw_image_path, raw_image_count)