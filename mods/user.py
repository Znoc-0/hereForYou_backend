from mods.db.db import user , bookings, professionals
import secrets

from flask import Flask, request, jsonify



def login_user(request):
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user_data = user.find_one({'email': email, 'password': password})
    # print(user_data)
    if not user_data:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    
    session_token = secrets.token_hex(16)
    user.update_one({'_id': user_data['_id']}, {'$set': {'session_token': session_token}})

    
    response = jsonify({
        'message': 'Login successful',
        'user': {
            'email': user_data['email'],
        }
    })
    response.set_cookie('session_token', session_token , httponly=True, secure=True)
    return response, 200


def register_user(request):
    data = request.json
    fullname = data.get('fullname')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')   
      # Default user type if not provided


    if not fullname or not password or not email or not phone:
        return jsonify({'error': 'All fields are required'}), 400
   
    if user.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 409
    if user.find_one({'phone': phone}):
        return jsonify({'error': 'Phone number already exists'}), 409
    
    new_user = {
        'fullname': fullname,
        'password': password,
        'email': email,
        'phone': phone
    }

    user.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

def get_professionals_info(request):
    data = request.json
    service_provided = data.get('service_provided')
    city = data.get('city')

    if not service_provided or not city:
        return jsonify({'error': 'service_provided and city are necessary'}), 400

    professional = list(professionals.find({'service_provided': service_provided , 'city': city}))

    if not professional or len(professional) == 0:
        return jsonify({'error': 'No professionals found for this service_provided and city'}), 404
    

    professionals_info = []
    for profession in professional:
        
        professional_info = {
            'professional_id': str(profession['_id']),
            'first_name': profession.get('first_name'),
            'last_name': profession.get('last_name'),
            'email': profession.get('email'),
            'phone': profession.get('phone'),
            'phone_number': profession.get('phone_number'),
            'date_of_birth': profession.get('date_of_birth'),
            'gender': profession.get('gender'),
            'address': profession.get('address'),
            'city': profession.get('city'),
            'pincode': profession.get('pincode'),
            'service_provided': profession.get('service_provided', []),
            'years_of_experience': profession.get('years_of_experience'),
            'hourly_rate': profession.get('hourly_rate'),
            'service_description': profession.get('service_description'),
           
        }
        professionals_info.append(professional_info)
    return jsonify({'professionals': professionals_info}), 200


def register_professional(request):
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    date_of_birth = data.get('date_of_birth') 
    gender = data.get('gender')
    address = data.get('address')
    city = city.lower(data.get('city'))
    pincode = data.get('pincode')
    service_provided = data.get('service_provided')
    years_of_experience = data.get('years_of_experience')
    hourly_rate = data.get('hourly_rate')
    service_description = data.get('service_description')
    bank_account_no = data.get('bank_account_no')
    bank_name = data.get('bank_name')
    ifsc_code = data.get('ifs_code')
    account_holder_name = data.get('account_holder_name')


    new_professional = {
        'email': email,
        'phone': phone,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'address': address,
        'city': city,
        'pincode': pincode,
        'service_provided': service_provided,
        'years_of_experience': years_of_experience,
        'hourly_rate': hourly_rate,
        'service_description': service_description,
        'bank_account_no': bank_account_no,
        'bank_name': bank_name,
        'ifs_code': ifsc_code,
        'account_holder_name': account_holder_name
        
    }

    professionals.insert_one(new_professional)

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
    
    userbooking= []
    for booking in user_bookings:
        booking_info = {
            'booking_id': booking.get('booking_id'),
            'professional_id': booking.get('professional_id'),
            'dates_and_times': booking.get('dates_and_times'),
            'full_address': booking.get('full_address'),
            'booking_date': booking.get('booking_date'),
            'booking_time': booking.get('booking_time'),
            'booking_status': booking.get('booking_status'),
            'pincode': booking.get('pincode'),
            'city': booking.get('city'),
            'service_type': booking.get('service_type'),
            'problem_description': booking.get('problem_description'),
            'urgency_level': booking.get('urgency_level'),
            'user_name': booking.get('user_name'),
            'user_phone': booking.get('user_phone'),
            'user_alternative_phone': booking.get('user_alternative_phone'),
            'special_instructions': booking.get('special_instructions')
        }
        userbooking.append(booking_info)

    if not userbooking:
        return jsonify({'message': 'No bookings found for this user'}), 404

    return jsonify({'bookings': userbooking}), 200


