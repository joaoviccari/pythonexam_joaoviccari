from get_single_location_reviews import get_business_and_reviews as get_br
import datetime

start = datetime.datetime.now()

locations = [
	['Sao Paulo', 'pizza'],
	('New York',),
	('Turim', 'bar'),
	('Montevideo',),
	(32.715736, -117.161087), # San Diego
	(42.361145, -71.057083, 'burgers'), # Boston
	(55.860916, -4.251433), # Glasgow
	(-22.9035, -43.2096, 'mcdonalds'), # Rio de Janeiro
	('Frankfurt',),
	('Cape Town', 'pasta')
]

for location in locations:
	if len(location) == 1:
		get_br(location=location[0])
	elif len(location) == 2:
		if isinstance(location[0], float):
			get_br(latitude=location[0], longitude=location[1])
		else:
			get_br(location=location[0], term=location[1])
	else:
		get_br(latitude=location[0], longitude=location[1], term=location[2])

end = datetime.datetime.now()

print(f'It took {end - start} to populate the database.')
