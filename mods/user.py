from mods.db.db import user

from flask import Flask, request, jsonify



def login_user(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user_data = user.find_one({'username': username, 'password': password})

    if not user_data:
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful', 'user': {'username': user_data['username']}}), 200



def register_user(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')

    if not username or not password or not email or not phone:
        return jsonify({'error': 'All fields are required'}), 400
    if user.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 409
    if user.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 409
    if user.find_one({'phone': phone}):
        return jsonify({'error': 'Phone number already exists'}), 409
    new_user = {
        'username': username,
        'password': password,
        'email': email,
        'phone': phone
    }

    user.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201