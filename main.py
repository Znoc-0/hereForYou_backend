from flask import Flask, request, jsonify
from flask_cors import CORS
from mods.user import login_user , register_user , get_professionals_info , register_professional,book_appointment,list_user_bookings
app = Flask(__name__)
CORS(app)

from mods.db.db import user, professionals, bookings
@app.route('/login', methods=['POST'])
def login():
   return login_user(request)

@app.route('/register', methods=['POST'])
def register():
    return register_user(request)

@app.route('/get_professionals', methods=['POST'])
def get_professionals():
    return get_professionals_info(request)

@app.route('/register_professional', methods=['POST'])
def registerProfessional():
    return register_professional(request)

@app.route('/booking', methods=['POST'])
def booking():
    return book_appointment(request)

@app.route('/list_bookings', methods=['POST'])
def list_bookings():
    return list_user_bookings(request)

if __name__ == '__main__':
    app.run(debug=True)