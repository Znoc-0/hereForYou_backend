from flask import Flask, request, jsonify
from flask_cors import CORS
from mods.user import login_user , register_user

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
   return login_user(request)

@app.route('/register', methods=['POST'])
def register():
    return register_user(request)

if __name__ == '__main__':
    app.run(debug=True)