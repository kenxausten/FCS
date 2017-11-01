#! /usr/bin/env python 
# -*- coding: utf-8 -*-

#Example https://github.com/0x024/MS

import urllib
import json
import os
import requests

class FacePlusServer(object):
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
	
if __name__ == '__main__':
	file_path = './ID1.jpg'
	faceSet_name = 'yy'
	face_plus_service = FacePlusServer(api_key='wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH', api_secret='wff5ht9ky77pWK52a_NtwY3Csz47CSqT')
	face_token_id = face_plus_service.get_img_token(file_path)
	if face_token_id:
		result = face_plus_service.set_create(faceSet_name)
		print result
		result = face_plus_service.set_add(faceSet_name, face_token_id)
		print result
		
		result = face_plus_service.search(faceSet_name, file_path)
		print result
	else:
		print "get image token failed"
# 	result = face_plus_service.set_delete(faceSet_name, 0)
	
# 	print result