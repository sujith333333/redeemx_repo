<<<<<<< HEAD
# RedeemX Web Application Backend

This project is a robust token management system designed for users and vendors. It includes features like points issuance, redemption, QR code integration, and secure authentication.

---

## **Getting Started**

### **Prerequisites**
Ensure you have the following installed on your system:
- Python 3.9+
- MySQL
- Git

---

## **Installation Steps**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd redeemx_de_app

### **2. Create and Activate a Virtual Environment**

#### **For Windows**
```bash
python -m venv venv
venv\Scripts\activate

#### **For WinmacOS/Linuxdows**
```bash

python3 -m venv venv
source venv/bin/activate

### **3. Install Dependencies**
```bash

pip install -r requirements.txt

### **4. Configure Environment Variables**
```ini
#Database
DB_HOST = ###
DB_NAME = redeemx_db
DB_USER = ###
DB_PASSWORD = ####
DB_PORT = 3306

# JWT settings
SECRET_KEY = ###  
ALGORITHM = ###
ACCESS_TOKEN_EXPIRE_MINUTES = ###

### **5. Run the FastAPI Application**
```bash

python3 src/main.py

##The API will be available at:

```cpp

http://127.0.0.1:8000




#### Technology
- **Python (FastAPI)**

#### Purpose
- Provides APIs for authentication, token management, redemption, and reporting.

#### Features
1. **User Login and Token Issuance**:
   - Secure user login.
   - Automatically awards 20 points on the first login of the day.
2. **QR Code Integration**:
   - Generates unique QR codes for vendors.
   - Validates QR codes during redemption.
3. **Token Validation and Transfer**:
   - Handles token validation and transactions between users and vendors.
4. **Token Expiry Management**:
   - Implements a scheduled task to expire tokens older than one month.

#### Database Design
- **Technology**: MySQL
- **Purpose**: User, vendor, and transaction data.
- **Tables/Collections**:
  - **Users**: `id`, `name`, `email`, `tokens`, `last_login`
  - **Vendors**: `id`, `name`, `qr_code`
  - **Transactions**: `id`, `user_id`, `vendor_id`, `timestamp`, `token_count`

---

## Dependencies Overview

### FastAPI and Related Libraries
- **`fastapi[standard]==0.115.6`**: The main framework for building APIs with Python, offering high performance and an intuitive interface.
- **`fastapi-pagination==0.12.34`**: Provides easy-to-implement pagination for API endpoints, essential for handling large datasets in a user-friendly way.
- **`fastapi-mail==1.4.2`**: A library for managing email notifications and communications, supporting features like attachments and templates.

### Database and ORM
- **`sqlmodel==0.0.22`**: Combines SQLAlchemy and Pydantic for database modeling and interaction, simplifying the creation of database schemas and CRUD operations.
- **`pymysql==1.1.1`**: A library for connecting to MySQL or MariaDB databases using Python.
- **`alembic==1.11.3`**: Used for database migrations to manage schema changes over time in a systematic way.

### Security and Authentication
- **`passlib==1.7.4`**: A comprehensive password hashing library that supports various hashing algorithms for secure authentication.
- **`bcrypt==4.2.1`**: A robust library for password hashing using the bcrypt algorithm.
- **`cryptography==44.0.0`**: Provides cryptographic recipes and primitives for securing sensitive data.
- **`PyJWT==2.10.1`**: A library for generating and validating JSON Web Tokens (JWT) for secure API authentication and user sessions.

### Real-Time Features
- **`websockets==11.0.3`**: Enables WebSocket support for implementing real-time features like live chat or notifications.

### Utility Libraries
- **`python-dotenv==1.0.0`**: Facilitates the management of environment variables using `.env` files, improving configuration handling.
- **`qrcode==7.3.1`**: A tool for generating QR codes, useful for features like secure sharing of information or quick data access.
- **`pillow==10.0.1`**: A library for image processing, supporting operations like resizing, filtering, and format conversion.
- **`loguru==0.7.0`**: A sophisticated logging library that simplifies logging in Python projects with structured outputs and advanced formatting.


## Project Structure (Backend)

```plaintext

redeemx_be_app/
├── src/
│   ├── user/                 # User module
│   │   ├── __init__.py
│   │   ├── routes.py         # User-related API routes
│   │   ├── models.py         # User models
│   │   ├── services.py       # User business logic
│   │   ├── dependencies.py   # User-specific dependencies
│   │   ├── schemas.py        # User Pydantic schemas
│   │   ├── tests/            # User test cases
│   │       ├── test_user.py
│   │
│   ├── vendor/               # Vendor module
│   │   ├── __init__.py
│   │   ├── routes.py         # Vendor-related API routes
│   │   ├── models.py         # Vendor models
│   │   ├── services.py       # Vendor business logic
│   │   ├── dependencies.py   # Vendor-specific dependencies
│   │   ├── schemas.py        # Vendor Pydantic schemas
│   │   ├── tests/            # Vendor test cases
│   │       ├── test_vendor.py
│   │
│   ├── transaction/          # Transaction module
│   │   ├── __init__.py
│   │   ├── routes.py         # Transaction-related API routes
│   │   ├── models.py         # Transaction models
│   │   ├── services.py       # Transaction business logic
│   │   ├── dependencies.py   # Transaction-specific dependencies
│   │   ├── schemas.py        # Transaction Pydantic schemas
│   │   ├── tests/            # Transaction test cases
│   │       ├── test_transaction.py
│   │
│   ├── auth/              # Shared dependencies
│   │   ├── __init__.py
│   │   ├── routes.py         # Auth-related API routes
│   │   ├── models.py         # Auth models
│   │   ├── services.py       # Auth business logic
│   │   ├── dependencies.py   # Auth-specific dependencies
│   │   ├── schemas.py        # Auth Pydantic schemas
│   │   ├── tests/            # Auth test cases
│   │       ├── test_transaction.py
│   │
│   ├── test/                # Test suite
│   │   ├── __init__.py
│   │   ├── test_main.py      # General tests
│   ├── __init__.py
│   ├── main.py               # Entry point for the FastAPI application
│   ├── config.py  
│   ├── database.py  
│   ├── exceptions.py  
│   ├── logging_config.py 
│   ├── models.py
│   ├── pagination.py 
│   ├── response.py
│   ├── scripts.py
│   ├── utils.py
│   
├── .env                      # Environment variables file
├── .gitignore                # Git ignore file
├── requirements.txt          # Backend dependencies
└── README.md                 # Documentation





=======
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
>>>>>>> 91001b01987aecb2a99258b197080bab71c317d7
