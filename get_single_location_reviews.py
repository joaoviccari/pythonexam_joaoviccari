import requests, json, pymongo, time
#import math

api_key = '2VK2TBy2esxU85VXaOUoQgYc4Qq3EuT39zREAcIs_WCT-i7378hngRQrLLITu9RsU1iPtGxkFMJymYZuuwaOQCK7tVJe2DVCmykQErYG40vGX_Q_a6MPS9HQzwYVYXYx'
headers = {
	'Authorization': 'Bearer %s' % api_key,
}
params = {'limit':50, 'sort_by':'review_count'}

def levenshtein_distance(business_name_1, business_name_2):
	if business_name_1 == "":
		return len(business_name_2)
	if not business_name_2:
		return len(business_name_1)
	if business_name_1[-1] == business_name_2[-1]:
		cost = 0
	else:
		cost = 1

	return min([
		levenshtein_distance(business_name_1[:-1], business_name_2) + 1,
		levenshtein_distance(business_name_1, business_name_2[:-1]) + 1, 
		levenshtein_distance(business_name_1[:-1], business_name_2[:-1]) + cost
	])

def get_business_and_reviews(location=None, latitude=None, longitude=None, term=None):
	collection_name = ''
	if location:
		params['location'] = location.lower()
		collection_name = params['location'].replace(' ', '_').replace('-', '').replace(',', '_')
	elif latitude and longitude:
		params['latitude'] = latitude
		params['longitude'] = longitude
		collection_name = '%f_%f' % (latitude, longitude)
	if term:
		params['term'] = term.lower()
		collection_name = '%s_%s' % (collection_name, params['term'])

	businesses_request = requests.get("https://api.yelp.com/v3/businesses/search", params=params, headers=headers)
	businesses = json.loads(businesses_request.text)

	if 'error' in businesses:
		print("\nWe're sorry! There were no businesses avaiable at given location or coordinates.")
	else:
		business_list = businesses['businesses']
		connection = pymongo.MongoClient('localhost', 27017)
		database = connection['businesses']
		business_collection_name = 'businesses_in_%s' % collection_name
		review_collection_name = 'reviews_in_%s' % collection_name
		if business_collection_name not in database.list_collection_names():
			business_collection = database[business_collection_name]
			reviews_collection = database[review_collection_name]
			bulk_insert_business_list = []
			bulk_insert_reviews_list = []
			for business in business_list:
				business_dict = {
					'business_id': business['id'],
					'business_name': business['name'],
					'business_adress': '%s - %s - %s - %s - %s' % (
						business['location']['address1'],
						business['location']['zip_code'],
						business['location']['city'],
						business['location']['state'],
						business['location']['country'],
					),
					'review_count': business['review_count'],
					'business_average_rating': business['rating'],
					'latitude': business['coordinates']['latitude'],
					'longitude': business['coordinates']['longitude'],
					'business_categories': [],
				}
				for category in business['categories']:
					business_dict['business_categories'].append(category['title'])
				bulk_insert_business_list.append(business_dict)
				reviews_request = requests.get('https://api.yelp.com/v3/businesses/%s/reviews' % business['id'], headers=headers)
				reviews = json.loads(reviews_request.text)
				if 'error' not in reviews:
					review_list = reviews['reviews']
					for review in review_list:
						review_dict = {
							'review_id': review['id'],
							'review_rating': review['rating'],
							'review_user_id': review['user']['id'],
							'review_user_name': review['user']['name'],
							'review_creation_time': review['time_created'],
							'review_text': review['text'],
							'business_reviewed_id': business['id'],
							'business_reviewed_name': business['name']
						}
						bulk_insert_reviews_list.append(review_dict)
			# levenshtein distance calculation:
			# for outer_business in bulk_insert_business_list:
			# 	shorter_levenshtein_distance = [math.inf, -1]
			# 	for index, inner_business in enumerate(bulk_insert_business_list):
			# 		if outer_business['business_name'] != inner_business['business_name']:
			# 			calculated_ld = levenshtein_distance(outer_business['business_name'], inner_business['business_name'])
			# 			if calculated_ld < shorter_levenshtein_distance[0]:
			# 				shorter_levenshtein_distance = [calculated_ld, index]
			# 	outer_business['most_similar_name_at_location'] = bulk_insert_business_list[shorter_levenshtein_distance[1]]['business_name']
			business_collection.insert_many(bulk_insert_business_list)
			reviews_collection.insert_many(bulk_insert_reviews_list)
		else:
			print('\n! ATTENTION: You already got information about businesses in this location. !')


if __name__ == '__main__':
	location, latitude, longitude, term = None, None, None, None
	valid_input = False

	while not valid_input:
		input_type = str(input("\nType in 'l' if you're entering a location or 'c' for coordinates: ")).lower()
		if input_type in ['c', 'l']:
			if input_type == 'l':
				location = ' '.join(str(input('\nEnter a location: ')).split()).strip()
			else:
				try:
					latitude = float(input("\nEnter latitude (decimal number separated by '.'): "))
					longitude = float(input("\nEnter longitude (decimal number separated by '.'): "))
				except ValueError:
					print('\n! ATTENTION: The coordinates you entered are not valid. !')
					time.sleep(2)
					continue
			term = str(input('\nAdditional term (leave blank if not necessary): '))
			get_business_and_reviews(location=location, latitude=latitude, longitude=longitude, term=term)
			valid_input = True
		else:
			print("\nPlease enter with 'l' or 'c'.")
			time.sleep(2)
