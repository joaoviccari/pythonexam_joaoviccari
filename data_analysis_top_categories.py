from collections import Counter
from csv import DictReader, DictWriter
import pymongo

connection = pymongo.MongoClient('localhost', 27017)
database = connection['top_categories_per_city']
top_categories_collection = database['top_categories']

with open('worldcities.csv', 'r', encoding='utf8') as input_file:
	csv_reader = DictReader(input_file)
	field_names = csv_reader.fieldnames
	with open('worldcities_top_categories.csv', 'w', encoding='utf8', newline='') as output_file:
		field_names.append('top_categories')
		csv_writer = DictWriter(output_file, fieldnames=field_names)
		csv_writer.writeheader()
		for city in csv_reader:
			row = city
			city_document = list(top_categories_collection.find({'city_name':city['city_ascii']}))
			if city_document:
				categories = Counter(city_document[0]['categories'])
				top_categories_set = set([category if categories[category] == categories[max(categories, key=categories.get)] else None for category in categories])
				if None in top_categories_set:
					top_categories_set.remove(None)
				top_categories = ','.join(top_categories_set)
				row['top_categories'] = top_categories
			else:
				row['top_categories'] = 'Not applicable'
			csv_writer.writerow(row)
