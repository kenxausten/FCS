#! /usr/bin/env python 
# -*- coding: utf-8 -*-

'''
Created on 2017/11/16

@author: Fucheng Xu
'''

import urllib
import json
import os
import requests
import cv2

class FaceService(object):
	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret
	
	def http_post(self, http_url, params, files=None):
		response_obj = requests.post(http_url, data=params, files=files)
		response_data = response_obj.content.decode('utf-8')
		response_data_json = json.loads(response_data)
		
		return response_data_json
	
	def detect(self, file_path):	
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'return_landmark': '1', 
			'return_attributes': 'gender,age'
		}
		files = {"image_file": open(file_path, "rb")}
	
		return self.http_post(http_url, params, files)
		
		#print response_obj.get('faces')[0]['face_token']
	
	def get_img_token(self, file_path):
		result = self.detect(file_path)
		try:
			res = result.get('faces')
			return res[0]['face_token']
		except Exception, e:
			print "Get Image Token Failed:(error:%s), (msg:%s)" % (e, result)
			return None
		
	def search(self, outer_id, file_path, return_result_count=1):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id, 
			'return_result_count': return_result_count
		}
		files = {"image_file": open(file_path, "rb")}
	
		return self.http_post(http_url, params, files)
	
	def set_create(self, outer_id, face_tokens=None, display_name=None, tags=None, force_merge=False, user_data=None):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id, 
			#TODO other params
		}
		
		return self.http_post(http_url, params, None)
	
	def set_add(self, outer_id, face_tokens):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id, 
			'face_tokens': face_tokens
		}
		
		return self.http_post(http_url, params, None)
	
	def set_remove(self, outer_id, face_tokens):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id, 
			'face_tokens': face_tokens
		}
		
		return self.http_post(http_url, params, None)
	
	def set_delete(self, outer_id, check_empty=1):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/delete'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id,
			'check_empty': check_empty
		}
		
		return self.http_post(http_url, params, None)
	
	def set_get(self):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
		}
		
		return self.http_post(http_url, params, None)
	
	def set_detail(self, outer_id):
		http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
			'outer_id': outer_id
		}
		
		return self.http_post(http_url, params, None)
	
def create_raw_faceset(face_service, faceset_name, image_path, image_count):
	result = face_service.set_create(faceset_name)
	token_file_name = {}
	for image_index in range(1, image_count+1):
		file_path = '%s/%d.jpg' % (image_path, image_index)
		token_id = face_service.get_img_token(file_path)
		if token_id:
			result = face_service.set_add(faceset_name, token_id)
			token_file_name[token_id] = file_path
	
	return token_file_name
			

def draw_face_location():
	face_service = FaceService(api_key='wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH', api_secret='wff5ht9ky77pWK52a_NtwY3Csz47CSqT')
<<<<<<< HEAD
	
	image_count = 4
	for image_index in range(1, image_count+1):
		file_path = '../image/%d.jpg' % image_index
		ret_file_path = '../image/face_%d.jpg' % image_index
		
		result = face_service.detect(file_path)
		print "image:%s, face count: %d" % (file_path, len(result["faces"]))
		
		img = cv2.imread(file_path)
		
		for i in range(0, len(result["faces"])):
			humanbody_rectangle = result["faces"][i]["face_rectangle"]
			x = humanbody_rectangle["left"]
			y = humanbody_rectangle["top"]
			w = humanbody_rectangle["width"]
			h = humanbody_rectangle["height"]
			z = str(i)
			print str(result["faces"][i])
			print
			img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 225, 225), 2)
			cv2.putText(img, z, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 100)
			
		cv2.imwrite(ret_file_path, img)

if __name__ == '__main__':	
# 	faceset_name = 'xx'
# 	
# 	raw_image_path = '../image/raw_image/'
# 	raw_image_count = 4
# 	
# 	file_path = '../image/11.jpg'
# 	face_service = FaceService(api_key='wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH', api_secret='wff5ht9ky77pWK52a_NtwY3Csz47CSqT')
#  	#token_file_name = create_raw_faceset(face_service, faceset_name, raw_image_path, raw_image_count)
# 	
# 	result = face_service.set_get()
# 	print result
# 	
# 	result = face_service.set_delete('yy', check_empty=0)
# 	print result
	
	draw_face_location()
	
# 	result = face_service.search(faceset_name, file_path, return_result_count=3)
# 	print result["results"]
# 	for i in range(len(result["results"])):
# 		print "token id:%s, confidence:%s" % (result["results"][i]["face_token"], result["results"][i]["confidence"])
# 	
# 	print token_file_name

# 	face_token_id = face_service.get_img_token(file_path)
# 	if face_token_id:
# 		result = face_service.set_create(faceSet_name)
# 		print result
# 		result = face_service.set_add(faceSet_name, face_token_id)
# 		print result
# 		
# 		result = face_service.search(faceSet_name, file_path)
# 		print result
# 	else:
# 		print "get image token failed"
# # 	result = face_service.set_delete(faceSet_name, 0)
# 	
# # 	print result