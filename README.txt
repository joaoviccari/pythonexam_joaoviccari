Concerning 'Data Analysis I', I considered populating the database using the cities in
'worldcities.csv', but that would take a lot of time to run. So for that step, I imagined
that the database content used to create the .csv output file would consider data coming
only from the usages of 'get_single_location_review.py' done beforehand on the 'Scraping'
stage.

So, to confirm that the file responsible for 'Data Analysis I' step (data_analysis_date.py)
does what is expected of it, please run 'populate_database.py'. It's a very small script I
wrote that runs 'get_business_and_reviews' method a few times for different locations and
distinct terms so that there is enough data to do the analysis. To expand the database, feel
free to add more tuples to the list of locations ('locations') using the following format:
    - (location,) or
    - (location, term,) or
    - (latitude, longitude,) or
    - (latitude, longitude, term,).

On the second data analysis I figured that I would need to create a database using data from the
41002 cities in the 'worldcities.csv' file. But, as only the categories from each business were
needed, I populated the database using documents with only the city name and its categories, 
since I assumed that it would save me some time if I didn't add other fields to the documents
besides the two mentioned. Still, it took my around 6 to 7 hours to estabilish a database for
'data_analysis_top_categories.py', which is why I exported that collection and uploaded it to
this git repository so that is possible to import it from MongoDB Compass and won't be necessary
to run 'populate_top_categories.py'.

Regarding the .kml file, I wasn't able to understand in the given time how to exactly work with
.kml data. I tried using the pykml package but didn't quite get how to extract the geographic
coordinates from that file.

Finally, for the Levenshtein Distance, which is used to find the greatest similarity between 
two business names, I used a recursive version of the algorithm, but it was too slow. For one
document with 50 business names, it was taking more than an hour to complete the calculations
of the Levenshtein Distances for the 50 of them. My implementation of Levenshtein Distance can
be found between lines 10 to 24 on the 'get_single_location_reviews.py' and its usage is in the
same file between lines 91 and 99. My intention was to find the business name closest to a fixed
business name and insert it into a field in the document.