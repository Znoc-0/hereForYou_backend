from pymongo import MongoClient

db = MongoClient('mongodb+srv://akshaysebastian777:BqL3ujW4EQNtsnOU@cluster0.7egr3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')['HereForYou']

user = db.user
bookings = db.bookings
professionals = db.professionals
