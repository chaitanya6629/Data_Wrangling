from pymongo import MongoClient
import os

print "Size of OSM File: ", (os.path.getsize(OSM_FILE))/(1024*1024), "MB"

print "Size of Sample File: ", (os.path.getsize(SAMPLE_FILE))/(1024*1024), "MB"

print "Number of documents = ", db.collection_houston.find().count()

print "Number of nodes = ", db.collection_houston.find({"type": "node"}).count()

print "Number of ways = ", db.collection_houston.find({"type": "way"}).count()

# Number of unique users:

pipeline1 = [{"$group": {"_id": "$created.uid"}}]
count = 0
for doc in db.collection_houston.aggregate(pipeline1):
    #pprint.pprint(doc)
    count = count+1
print "Number of Unique Users = ", count

# Top 10 users with maximum contribution:

pipeline2 = [{"$group": {"_id": "$created.user", "number_of_contributions": {"$sum": 1}}},
            {"$sort": {"number_of_contributions": -1}},
            {"$limit": 10}]
print "Top 10 users with maximum contribution:"
for doc in db.collection_houston.aggregate(pipeline2):
    pprint.pprint(doc)

	
# Top 10 users with most contribution:

pipeline2 = [{"$group": {"_id": "$created.user", "number_of_contributions": {"$sum": 1}}},
            {"$sort": {"number_of_contributions": -1}},
            {"$limit": 10}]
print "Top 10 users with most contribution:"
for doc in db.collection_houston.aggregate(pipeline2):
    pprint.pprint(doc)

# Top 10 popular cuisines in Houston:

pipeline3 = [{"$match": {"cuisine": {"$ne": None}}},
    {"$group": {"_id": "$cuisine", "freq": {"$sum": 1}}},
            {"$sort": {"freq": -1}},
            {"$limit": 10}]
print "Top 10 popular cuisines in Houston:"			
for doc in db.collection_houston.aggregate(pipeline3):
    pprint.pprint(doc)
	
	
# Top 10 most popular amenities:

pipeline4 = [{"$match": {"amenity": {"$ne": None}}},
    {"$group": {"_id": "$amenity", "freq": {"$sum": 1}}},
            {"$sort": {"freq": -1}},
            {"$limit": 10}]
print "Top 10 most popular amenities:"
for doc in db.collection_houston.aggregate(pipeline4):
    pprint.pprint(doc)

	
