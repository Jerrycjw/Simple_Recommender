import math
from pymongo import MongoClient
from dataservice import DataService
import operator
class Helper(object):
	@classmethod
	def cosine_similarity(cls, app_list1, app_list2):
	##Calculate cosine_similarity between 2 user's (download) applist
		match_count = cls.__count_match(app_list1,app_list2)
		return float(match_count) / math.sqrt(len(app_list1)*len(app_list2))
	@classmethod
	def __count_match(cls, list1, list2):
	##Count how many apps matched in 2 user's (download) applist
		count = 0
		for element in list1:
			if element in list2:
				count += 1
		return count
def calculate_Top_5(app, user_download_history):
	##For one app find out top 5 similar apps
	app_similarity = {}
	for apps in user_download_history:
		similarity = Helper.cosine_similarity([app],apps)
		for other_app in apps:
			if other_app in app_similarity:
				app_similarity[other_app] = app_similarity[other_app]+similarity
			else:
				app_similarity[other_app] = similarity
	if app not in app_similarity:
		return
	app_similarity.pop(app)##Pop itself
	sorted_tups = sorted(app_similarity.items(), key=operator.itemgetter(1), reverse=True)
	top_5_app = [sorted_tups[0][0], sorted_tups[1][0], sorted_tups[2][0], sorted_tups[3][0], sorted_tups[4][0]]
	print ("Top 5 App for "+ str(app) +":\t" + str(top_5_app))
	return top_5_app

def main():
	try:
		client = MongoClient('localhost',27017)
		DataService.init(client)
		apps = DataService.retrieve_appinfo()
		#work flow

		for app in apps.keys():
			user_download_history = DataService.retrieve_user_download_history()
			top_5_app = calculate_Top_5(app, user_download_history.values())
			DataService.update_app_info({"app_id": app},{"$set": {"Top 5": top_5_app}})
	except Exception as e:
		print(e)
	finally:
		#clean up work
		if 'client' in locals():
			client.close()

if __name__ == '__main__':
	main()
