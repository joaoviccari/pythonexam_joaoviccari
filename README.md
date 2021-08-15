Concerning 'Data Analysis I', I considered populating the database using the cities in 'worldcities.csv',
but that would take a lot of time to run. So for that step, I imagined that the database content used to
create the .csv output file would consider data coming only from the usages of 'get_single_location_review.py'
done beforehand on the 'Scraping' stage.

So, to confirm that the file responsible for 'Data Analysis I' step (data_analysis_date.py) does what is
expected of it, please run 'populate_database.py'. It's a very small script I wrote that runs 
'get_business_and_reviews' method a few times for different locations and distinct terms so that there is
enough data to do the analysis. To expand the database, feel free to add more tuples to the list of
locations ('locations') using the following format:
    - (location,) or
    - (location, term,) or
    - (latitude, longitude,) or
    - (latitude, longitude, term,).