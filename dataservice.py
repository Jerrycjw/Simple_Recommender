from pymongo import MongoClient
import random

class DataService(object):
#Dealing with data service from MongoDB
	@classmethod
	def init(cls, client):
	#initializing the connection to MongoDB
		cls.client = client
		cls.db = client.appstore
		cls.user_download_history = cls.db.user_download_history
		cls.app_info = cls.db.app_info
	@classmethod 
	def retrieve_user_download_history(cls, filter_dict={}):
		#retrieve user download history from mongodb
		result = {}
		cursor = cls.user_download_history.find(filter_dict)
		for user_download_history in cursor:
			result[user_download_history['user_id']] = user_download_history['download_history']
		return result
	@classmethod
	def retrieve_appinfo(cls, filter_dict={}):
		#retrieve specific app information
		result = {}
		cursor = cls.app_info.find(filter_dict)
		for app_info in cursor:
			result[app_info['app_id']] = {'title':app_info['title']}
		return result
	@classmethod
	def update_app_info(cls, filter_dict, update):
		#update specific item with filter_dict using update command,
		#which is defined by update variable
		cls.app_info.update_one(filter_dict, update, True)

