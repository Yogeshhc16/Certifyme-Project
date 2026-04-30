from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import uuid
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

# ================= MODELS =================

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    skills = db.Column(db.String(200))
    category = db.Column(db.String(50))
    future_opportunities = db.Column(db.String(200))
    max_applicants = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)

# ================= LOGIN MANAGER =================

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ================= SIGNUP =================

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email').lower()
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # validations
    if not full_name or not email or not password or not confirm_password:
        return jsonify({"error": "All fields required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # ✅ STRONG PASSWORD VALIDATION
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(pattern, password):
        return jsonify({
            "error": "Password must contain uppercase, lowercase, number and special character"
        }), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Account already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_admin = Admin(
        full_name=full_name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Signup successful"})

# ================= LOGIN =================

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email').lower()
    password = data.get('password')
    remember = data.get('remember', False)

    admin = Admin.query.filter_by(email=email).first()

    if admin and bcrypt.check_password_hash(admin.password, password):
        login_user(admin, remember=remember)
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid email or password"}), 401

# ================= FORGOT PASSWORD =================

reset_tokens = {}

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if email:
        user = Admin.query.filter_by(email=email).first()
        if user:
            token = str(uuid.uuid4())
            reset_tokens[token] = {
                "email": email,
                "expires": datetime.utcnow() + timedelta(hours=1)
            }
            print("RESET LINK:", f"http://localhost:5000/reset/{token}")

    return jsonify({"message": "If the email exists, a reset link has been sent"})

# ================= ADD OPPORTUNITY =================

@app.route('/add-opportunity', methods=['POST'])
def add_opportunity():
    if not current_user.is_authenticated:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()

    new_opportunity = Opportunity(
        name=data.get('name'),
        duration=data.get('duration'),
        start_date=data.get('start_date'),
        description=data.get('description'),
        skills=data.get('skills'),
        category=data.get('category'),
        future_opportunities=data.get('future_opportunities'),
        max_applicants=data.get('max_applicants'),
        admin_id=current_user.id
    )

    db.session.add(new_opportunity)
    db.session.commit()

    return jsonify({"message": "Opportunity added successfully"})

# ================= GET OPPORTUNITIES =================

@app.route('/get-opportunities', methods=['GET'])
def get_opportunities():
    if not current_user.is_authenticated:
        return jsonify({"error": "Login required"}), 401

    opportunities = Opportunity.query.filter_by(admin_id=current_user.id).all()

    result = []
    for o in opportunities:
        result.append({
            "id": o.id,
            "name": o.name,
            "duration": o.duration,
            "start_date": o.start_date,
            "description": o.description,
            "skills": o.skills,
            "category": o.category,
            "future_opportunities": o.future_opportunities,
            "max_applicants": o.max_applicants
        })

    return jsonify(result)

# ================= UPDATE OPPORTUNITY =================

@app.route('/update-opportunity/<int:id>', methods=['PUT'])
def update_opportunity(id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Login required"}), 401

    opportunity = Opportunity.query.get(id)

    if not opportunity or opportunity.admin_id != current_user.id:
        return jsonify({"error": "Not allowed"}), 403

    data = request.get_json()

    opportunity.name = data.get('name')
    opportunity.duration = data.get('duration')
    opportunity.start_date = data.get('start_date')
    opportunity.description = data.get('description')
    opportunity.skills = data.get('skills')
    opportunity.category = data.get('category')
    opportunity.future_opportunities = data.get('future_opportunities')
    opportunity.max_applicants = data.get('max_applicants')

    db.session.commit()

    return jsonify({"message": "Updated successfully"})

# ================= DELETE OPPORTUNITY =================

@app.route('/delete-opportunity/<int:id>', methods=['DELETE'])
def delete_opportunity(id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Login required"}), 401

    opportunity = Opportunity.query.get(id)

    if not opportunity or opportunity.admin_id != current_user.id:
        return jsonify({"error": "Not allowed"}), 403

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})

# ================= RUN =================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)