import csv, pymongo, datetime, statistics

valid_date = False

while not valid_date:
	try:
		date = str(input('Enter date in the format (YYYY-MM-DD): '))
		year = int(date[0:4])
		month = int(date[5:7])
		day = int(date[8:10])
		valid_date = True
	except ValueError:
		print('Please, enter a valid date in the following format: YYYY-MM-DD.')

connection = pymongo.MongoClient()
database = connection['businesses']

date = datetime.datetime(year, month, day)

with open('business_reviews_statistics.csv', 'w', newline='') as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(['business_id', 'business_name', 'city', 'state', 'reviews_since_date', 'mean', 'standard deviation', 'median', 'mode'])
	for business_collection_name in database.list_collection_names():
		if business_collection_name not in ['admin', 'config', 'local'] and business_collection_name.startswith('businesses_in_'):
			location = business_collection_name.split('_in_')
			review_collection_name = 'reviews_in_%s' % location[1]
			business_collection_list = list(database[business_collection_name].find({}))
			for business in business_collection_list:
				business_adress_list = business['business_adress'].split(' - ')
				city, state = business_adress_list[2], business_adress_list[3]
				row = [business['business_id'], business['business_name'], city, state]
				valid_reviews = []
				review_collection_list = list(database[review_collection_name].find({'business_reviewed_id':business['business_id']}))
				if len(review_collection_list) > 0:
					for review in review_collection_list:
						year, month, day = review['review_creation_time'].split(' ')[0].split('-')
						review_date = datetime.datetime(int(year), int(month), int(day))
						if review_date > date:
							valid_reviews.append(review['review_rating'])
				row.append(len(valid_reviews))
				if valid_reviews:
					row.extend([
						round(statistics.mean(valid_reviews), 4),
						round(statistics.stdev(valid_reviews), 4) if len(valid_reviews) > 1 else 'Not applicable',
						statistics.median(valid_reviews),
						statistics.mode(valid_reviews)
					])
				else:
					row.extend(['Not applicable', 'Not applicable', 'Not applicable', 'Not applicable'])
				csv_writer.writerow(row)
