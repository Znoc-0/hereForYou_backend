from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


mongo_url = os.getenv("MONGO_URL")
db = MongoClient(mongo_url)['HereForYou']


user = db.user


bookings = db.bookings
professionals = db.professionals




    