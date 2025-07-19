from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/')['HereForYou']

user = db.user
bookings = db.bookings
professionals = db.professionals
