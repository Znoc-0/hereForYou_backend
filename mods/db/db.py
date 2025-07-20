from pymongo import MongoClient

db = MongoClient('MONGOURL')['HereForYou']

user = db.user
bookings = db.bookings
professionals = db.professionals
