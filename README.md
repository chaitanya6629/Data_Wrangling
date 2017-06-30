# Data_Wrangling
Use data munging techniques to assess data for validity, accuracy, completeness, consistency and uniformity on OpenStreetMap data.

Files:

*** Project_Data_Wrangling.html is the html version of the entire notebook. It contains all the code and results. 
    I have also included the .ipynb and .py versions of the same.

1.) sample.py
	Creates sample file

2.) analyze_tags.py
	Analyzes the tag values

3.) analyze_keys.py
	Analyzes the keys in tags

4.) tags.py
	Analyzes tag patterns

5.) audit.py
	This file audits all the fields (street, city, housenumber, postcode, state). 
	Then, it stores all the incorrect/invalid entries in respective lists/dictionaries, which will be used by the cleaning functions.

6.) improve_city_name.py, improve_house_number.py, improve_postcode.py, improve_state.py, improve_street_name.py
	These files contain the cleaning functions for the respective fields.

7.) data.py
	Shapes the elements, stores the cleaned data in json file.

8.) database.py
	Creates database and inserts the cleaned data into MongoDB.

9.) queries.py
	MongoDB queries for exploring the database.

10.) map.txt
	Contains the link to the map position for Houston,TX

11.) houston_texas_small_sample.osm
	An .osm file containing a sample part of the map region I used.
