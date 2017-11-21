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

class BodyService(object):
	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret
	
	def http_post(self, http_url, params, files=None):
		response_obj = requests.post(http_url, data=params, files=files)
		response_data = response_obj.content.decode('utf-8')
		response_data_json = json.loads(response_data)
		
		return response_data_json
	
	def detect(self, file_path):	
		http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/detect'
		params = {
			'api_key': self.api_key, 
			'api_secret': self.api_secret, 
		}
		files = {"image_file": open(file_path, "rb")}
	
		return self.http_post(http_url, params, files)
		
		#print response_obj.get('faces')[0]['face_token']
	
if __name__ == '__main__':
	
	body_service = BodyService(api_key='wCadfoQIEbZ1RvksVWvlTkd21a5bZWAH', api_secret='wff5ht9ky77pWK52a_NtwY3Csz47CSqT')
	
	image_count = 4
	for image_index in range(1, image_count+1):
		file_path = '../image/%d.jpg' % image_index
		ret_file_path = '../image/body_%d.jpg' % image_index
		
		result = body_service.detect(file_path)
		print "image:%s, body count: %d" % (file_path, len(result["humanbodies"]))
		
		img = cv2.imread(file_path)
		
		for i in range(0, len(result["humanbodies"])):
			humanbody_rectangle = result["humanbodies"][i]["humanbody_rectangle"]
			x = humanbody_rectangle["left"]
			y = humanbody_rectangle["top"]
			w = humanbody_rectangle["width"]
			h = humanbody_rectangle["height"]
			z = str(i)
			img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 225, 225), 2)
			cv2.putText(img, z, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 100)
			
		cv2.imwrite(ret_file_path, img)