from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017/')
db = client.houston
db.collection_houston.insert(data)
