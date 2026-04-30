#  CertifyMe – Admin Portal for Opportunity Management

A full-stack web application that allows administrators to manage opportunities such as internships, courses, and programs. Built using **Flask (Python)** for the backend and **HTML, CSS, JavaScript** for the frontend.

---

## 🚀 Features

### 🔐 Authentication

* Admin Sign Up with strong password validation
* Secure Login using hashed passwords (Flask-Bcrypt)
* Forgot Password (token-based reset system)

### 📊 Opportunity Management

* View all opportunities
* Add new opportunities
* Edit existing opportunities
* Delete opportunities
* Data persists after login

### 🔒 Security Features

* Password hashing using bcrypt
* Strong password validation (uppercase, lowercase, number, special character)
* Session-based authentication (Flask-Login)
* Protected routes (only logged-in admins can access)

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Bcrypt
* Flask-CORS

### Frontend

* HTML
* CSS
* JavaScript (Fetch API)

### Database

* SQLite (auto-created)

---

## 📁 Project Structure

```
certifyme/
│
├── app.py               # Main Flask backend
├── instance/
│   └── database.db     # SQLite database (auto-created)
│
├── templates/
│   └── admin.html      # Admin UI
│
├── static/
│   ├── script.js
│   ├── admin.js
│   └── admin.css
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/certifyme.git
cd certifyme
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install flask flask-sqlalchemy flask-login flask-bcrypt flask-cors
```

### 4️⃣ Run the application

```bash
python app.py
```

---

## 🌐 API Endpoints

### 🔐 Auth

* `POST /signup` → Create admin account
* `POST /login` → Login
* `POST /forgot-password` → Reset password

### 📌 Opportunities

* `POST /add-opportunity` → Add opportunity
* `GET /get-opportunities` → Get all
* `PUT /update-opportunity/<id>` → Update
* `DELETE /delete-opportunity/<id>` → Delete

---

## 🔑 Password Rules

Password must contain:

* At least 8 characters
* One uppercase letter
* One lowercase letter
* One number
* One special character

Example:

```
Yogesh@2004
```

---

## 📸 Screenshots

* Admin Signup Page
* Admin Login Page
* Dashboard
* Opportunity Management

(Add your screenshots here)

---

## 🧠 Future Improvements

* Email-based password reset
* JWT authentication
* Role-based access control
* Deployment (AWS / Render / Railway)
* UI enhancements

---

## 👨‍💻 Author

**Yogesh HC**

---

## 📄 License

This project is open-source and available under the MIT License.
