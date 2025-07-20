
  # API Documentation

  ---

  ## Method [POST]   Base_url/login

  ### Description
  Authenticate a user by email and password. Returns a secure session token cookie and user info on success.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
  - **Body:**

  | Parameter | Type   | Required | Description            |
  | --------- | ------ | -------- | ---------------------- |
  | email     | string | Yes      | Registered user email  |
  | password  | string | Yes      | User's password        |

  **Example:**
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

  ### Responses

  - **200 OK**

  ```json
  {
    "message": "Login successful",
    "user": {
      "email": "user@example.com"
    }
  }
  ```

  - Sets a secure, HttpOnly cookie: `session_token`

  - **400 Bad Request**

  ```json
  {
    "error": "Email and password are required"
  }
  ```

  - **401 Unauthorized**

  ```json
  {
    "error": "Invalid email or password"
  }
  ```

  ---

  ## Method [POST] Base_url/register

  ### Description
  Register a new user with fullname, email, password, and phone.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
  - **Body:**

  | Parameter | Type   | Required | Description              |
  | --------- | ------ | -------- | ------------------------ |
  | fullname  | string | Yes      | Full name of the user    |
  | email     | string | Yes      | User's email             |
  | password  | string | Yes      | User's password          |
  | phone     | string | Yes      | User's phone number      |

  **Example:**
  ```json
  {
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securepassword",
    "phone": "1234567890"
  }
  ```

  ### Responses

  - **201 Created**

  ```json
  {
    "message": "User registered successfully"
  }
  ```

  - **400 Bad Request**

  ```json
  {
    "error": "All fields are required"
  }
  ```

  - **409 Conflict**

  ```json
  {
    "error": "Email already exists"
  }
  ```

  or

  ```json
  {
    "error": "Phone number already exists"
  }
  ```

  ---

  ## Method [POST] Base_url/get_professionals

  ### Description
  Get a list of professionals filtered by `service_provided` and `city`.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
  - **Body:**

  | Parameter        | Type   | Required | Description                            |
  | ---------------- | ------ | -------- | ------------------------------------ |
  | service_provided  | string | Yes      | The service offered by professionals |
  | city             | string | Yes      | City name                            |

  **Example:**
  ```json
  {
    "service_provided": "plumbing",
    "city": "New York"
  }
  ```

  ### Responses

  - **200 OK**

  ```json
  {
    "professionals": [
      {
        "professional_id": "60f7b9a6...",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone": "9876543210",
        "phone_number": "9876543210",
        "date_of_birth": "1990-01-01",
        "gender": "female",
        "address": "123 Main St",
        "city": "New York",
        "pincode": "10001",
        "service_provided": ["plumbing", "heating"],
        "years_of_experience": 5,
        "hourly_rate": 50,
        "service_description": "Experienced plumber"
      }
    ]
  }
  ```

  - **400 Bad Request**

  ```json
  {
    "error": "service_provided and city are necessary"
  }
  ```

  - **404 Not Found**

  ```json
  {
    "error": "No professionals found for this service_provided and city"
  }
  ```

  ---

  ## Method [POST] Base_url/register_professional

  ### Description
  Register a new professional with detailed info including bank details.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
  - **Body:**

  | Parameter             | Type     | Required | Description                     |
  | --------------------- | -------- | -------- | -------------------------------|
  | email                 | string   | Yes      | Professional's email            |
  | phone                 | string   | Yes      | Phone number                   |
  | first_name            | string   | Yes      | First name                    |
  | last_name             | string   | Yes      | Last name                     |
  | phone_number          | string   | Yes      | Contact phone number           |
  | date_of_birth         | string   | Yes      | Date of birth (ISO format)     |
  | gender                | string   | Yes      | Gender                        |
  | address               | string   | Yes      | Address                       |
  | city                  | string   | Yes      | City (converted to lowercase)  |
  | pincode               | string   | Yes      | Postal code                   |
  | service_provided      | string   | Yes      | Service(s) provided           |
  | years_of_experience   | number   | Yes      | Years of experience           |
  | hourly_rate           | number   | Yes      | Hourly rate charged           |
  | service_description   | string   | Yes      | Description of services       |
  | bank_account_no       | string   | Yes      | Bank account number           |
  | bank_name             | string   | Yes      | Bank name                    |
  | ifs_code              | string   | Yes      | IFSC code                    |
  | account_holder_name   | string   | Yes      | Bank account holder's name    |

  **Example:**
  ```json
  {
    "email": "pro@example.com",
    "phone": "1234567890",
    "first_name": "Bob",
    "last_name": "Jones",
    "phone_number": "1234567890",
    "date_of_birth": "1985-05-05",
    "gender": "male",
    "address": "456 Elm St",
    "city": "los angeles",
    "pincode": "90001",
    "service_provided": "electrical",
    "years_of_experience": 10,
    "hourly_rate": 75,
    "service_description": "Certified electrician",
    "bank_account_no": "123456789012",
    "bank_name": "Bank of America",
    "ifs_code": "BOFAUS3N",
    "account_holder_name": "Bob Jones"
  }
  ```

  ### Responses

  - **201 Created**

  ```json
  {
    "message": "Professional registered successfully"
  }
  ```

  ---

  ## Method [POST] Base_url/booking

  ### Description
  Book an appointment with a professional. Requires user authentication via session cookie.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
    - Cookie: `session_token=<token>`
  - **Body:**

  | Parameter             | Type     | Required | Description                         |
  | --------------------- | -------- | -------- | ----------------------------------|
  | professional_id       | string   | Yes      | ID of the professional to book     |
  | dates_and_times       | array    | Yes      | Array of date and time slots       |
  | full_address          | string   | Yes      | Full address for the appointment   |
  | booking_date          | string   | Optional | Date of booking                    |
  | booking_time          | string   | Optional | Time of booking                    |
  | pin_code              | string   | Optional | Postal code                       |
  | city                  | string   | Optional | City name                        |
  | service_type          | string   | Optional | Type of service                   |
  | problem_description   | string   | Optional | Description of the problem        |
  | urgency_level         | string   | Optional | Urgency level                    |
  | user_name             | string   | Optional | Name of user                     |
  | user_phone            | string   | Optional | User phone number                |
  | user_alternative_phone| string   | Optional | Alternative phone number         |
  | special_instructions  | string   | Optional | Additional instructions          |

  **Example:**
  ```json
  {
    "professional_id": "60f7b9a6f3a2c5b3d1234567",
    "dates_and_times": ["2025-08-25T10:00", "2025-08-26T14:00"],
    "full_address": "789 Pine St, Apt 4",
    "booking_date": "2025-08-24",
    "booking_time": "10:00",
    "pin_code": "123456",
    "city": "New York",
    "service_type": "plumbing",
    "problem_description": "Leaky faucet",
    "urgency_level": "medium",
    "user_name": "John Doe",
    "user_phone": "9876543210",
    "user_alternative_phone": "9876543211",
    "special_instructions": "Please call on arrival"
  }
  ```

  ### Responses

  - **201 Created**

  ```json
  {
    "message": "Appointment booked successfully",
    "booking_id": "a1b2c3d4e5f6g7h8"
  }
  ```

  - **400 Bad Request**

  ```json
  {
    "error": "All fields are required"
  }
  ```

  - **401 Unauthorized**

  ```json
  {
    "error": "Unauthorized"
  }
  ```

  or

  ```json
  {
    "error": "Invalid session token"
  }
  ```

  ---

  ## Method [POST] Base_url/list_bookings

  ### Description
  List all bookings of the authenticated user.

  ### Request

  - **Headers:**
    - `Content-Type: application/json`
    - Cookie: `session_token=<token>`

  ### Responses

  - **200 OK**

  ```json
  {
    "bookings": [
      {
        "booking_id": "a1b2c3d4e5f6g7h8",
        "professional_id": "60f7b9a6f3a2c5b3d1234567",
        "dates_and_times": ["2025-08-25T10:00", "2025-08-26T14:00"],
        "full_address": "789 Pine St, Apt 4",
        "booking_date": "2025-08-24",
        "booking_time": "10:00",
        "booking_status": "pending",
        "pincode": "123456",
        "city": "New York",
        "service_type": "plumbing",
        "problem_description": "Leaky faucet",
        "urgency_level": "medium",
        "user_name": "John Doe",
        "user_phone": "9876543210",
        "user_alternative_phone": "9876543211",
        "special_instructions": "Please call on arrival"
      }
    ]
  }
  ```

  - **401 Unauthorized**

  ```json
  {
    "error": "Unauthorized"
  }
  ```

  or

  ```json
  {
    "error": "Invalid session token"
  }
  ```

  - **404 Not Found**

  ```json
  {
    "message": "No bookings found for this user"
  }
  ```

  ---

  # Notes

  - All POST endpoints expect `Content-Type: application/json`.
  - Authentication for booking-related endpoints uses a secure, HTTP-only `session_token` cookie.
  - Passwords are currently handled in plain text — it is **highly recommended** to hash passwords securely (e.g., bcrypt) before storing or comparing.
  - The `city` parameter for professionals is stored in lowercase internally for consistency.

