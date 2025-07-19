from mods.db.db import user , bookings, professionals
import secrets

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
    
    
    session_token = secrets.token_hex(16)
    user.update_one({'_id': user_data['_id']}, {'$set': {'session_token': session_token}})

    
    response = jsonify({
        'message': 'Login successful',
        'user': {
            'username': user_data['username'],
        }
    })
    response.set_cookie('session_token', session_token)

    return response, 200


def register_user(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')   
    user_type = data.get('user_type')  # Default user type if not provided


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
        'user_type': user_type,  # Default user type
        'email': email,
        'phone': phone
    }

    user.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

def get_professionals_info(request):
    data = request.json
    profession = data.get('profession')

    if not profession:
        return jsonify({'error': 'Profession is required'}), 400

    professionals = list(user.find({'profession': profession}))

    if not professionals:
        return jsonify({'error': 'No professionals found for this profession'}), 404

    professionals_info = []
    for professional in professionals:
        professional_info = {
            'name': professional.get('name'),
            'place': professional.get('place'),
            'rating': professional.get('rating'),
            'reviews': professional.get('reviews', []),
            'experience': professional.get('experience'),
            'rate_of_service': professional.get('rate_of_service', {}),  # Fetch entire rate_of_service dictionary from DB
            'distance': professional.get('distance'),
            'specialities': professional.get('specialities', []),
            'is_available': professional.get('is_available', False),
            'certifications': professional.get('certifications', []),
            'years_of_experience': professional.get('years_of_experience'),
            'services': professional.get('services', []),
        }
        professionals_info.append(professional_info)
    return jsonify({'professionals': professionals_info}), 200


def register_professional(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    profession = data.get('profession')

    if not username or not password or not email or not phone or not profession:
        return jsonify({'error': 'All fields are required'}), 400

    if user.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 409
    if user.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 409
    if user.find_one({'phone': phone}):
        return jsonify({'error': 'Phone number already exists'}), 409

    new_professional = {
        'username': username,
        'password': password,
        'email': email,
        'phone': phone,
        'profession': profession,
        'user_type': 'professional'  # Set user type as professional
    }

    user.insert_one(new_professional)

    return jsonify({'message': 'Professional registered successfully'}), 201


def book_appointment(request):
    data = request.json
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_data = user.find_one({'session_token': session_token})
    if not user_data:
        return jsonify({'error': 'Invalid session token'}), 401
    
    booking_details = {
        'user_id': user_data['_id'],
        'professional_id': data.get('professional_id'),
        'dates_and_times': data.get('dates_and_times'),
        'full_address': data.get('full_address'),
        'booking_date': data.get('booking_date'),
        'booking_time': data.get('booking_time'),
        'booking_status': 'pending',
        'pincode': data.get('pin_code'),
        'city': data.get('city'),
        'service_type': data.get('service_type'),
        'problem_description': data.get('problem_description'),
        'urgency_level': data.get('urgency_level'),
        'user_name': data.get('user_name'),
        'user_phone': data.get('user_phone'),
        'user_alternative_phone': data.get('user_alternative_phone'),
        'special_instructions': data.get('special_instructions'),
        'booking_id': secrets.token_hex(8)  # Generate a unique booking ID
    }

    if not booking_details['professional_id'] or not booking_details['dates_and_times'] or not booking_details['full_address']:
        return jsonify({'error': 'All fields are required'}), 400
    

    bookings.insert_one(booking_details)

    return jsonify({'message': 'Appointment booked successfully', 'booking_id': booking_details['booking_id']}), 201



def get_user_by_session_token(session_token):
    return user.find_one({'session_token': session_token})


def list_user_bookings(request):
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_data = get_user_by_session_token(session_token)
    if not user_data:
        return jsonify({'error': 'Invalid session token'}), 401
    
    user_bookings = list(bookings.find({'user_id': user_data['_id']}))

    if not user_bookings:
        return jsonify({'message': 'No bookings found for this user'}), 404

    return jsonify({'bookings': user_bookings}), 200


