import requests, json, pymongo
from csv import DictReader

api_key = '2VK2TBy2esxU85VXaOUoQgYc4Qq3EuT39zREAcIs_WCT-i7378hngRQrLLITu9RsU1iPtGxkFMJymYZuuwaOQCK7tVJe2DVCmykQErYG40vGX_Q_a6MPS9HQzwYVYXYx'
headers = {
	'Authorization': 'Bearer %s' % api_key,
}
params = {'limit':50, 'sort_by':'review_count'}

connection = pymongo.MongoClient('localhost', 27017)
database = connection['top_categories_per_city']
top_categories_collection = database['top_categories']

with open('worldcities.csv', 'r', encoding='utf8') as file:
	csv_reader = DictReader(file)
	documents_to_be_inserted = []
	for location in csv_reader:
		params['location'] = location['city_ascii']
		city_dict = {
			'city_name': location['city_ascii'],
			'categories': []
		}
		location_request = requests.get("https://api.yelp.com/v3/businesses/search", params=params, headers=headers)
		businesses = json.loads(location_request.text)		
		if 'error' in businesses:
			print(f"\nWe're sorry! There were no businesses avaiable at given location: {location['city_ascii']}")
		else:
			business_list = businesses['businesses']
			for business in business_list:
				for category in business['categories']:
					city_dict['categories'].append(category['title'])
			documents_to_be_inserted.append(city_dict)
	top_categories_collection.insert_many(documents_to_be_inserted)
