from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.models import db, User

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    # Simple email validation
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    qualification = data.get('qualification', '').strip()
    role = 'user'

    # Validate all fields
    if not name:
        return jsonify({'message': 'Name is required.'}), 400
    if not email:
        return jsonify({'message': 'Email is required.'}), 400
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format.'}), 400
    if not password:
        return jsonify({'message': 'Password is required.'}), 400
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long.'}), 400
    if not qualification:
        return jsonify({'message': 'Qualification is required.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered.'}), 409

    # Generate hashed password and save to model
    password_hash = generate_password_hash(password)
    user = User(
        name=name,
        email=email,
        qualification=qualification,
        role=role,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validate all fields
    if not email:
        return jsonify({'message': 'Email is required.'}), 400
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format.'}), 400
    if not password:
        return jsonify({'message': 'Password is required.'}), 400
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid email or password.'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role, 'name': user.name, 'email': user.email})
    return jsonify({'access_token': access_token, 'user': {
        'id': user.id,
        'role': user.role,
        'email': user.email,
        'name': user.name,
    }}), 200

from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_bp.route('/profile/<int:userid>', methods=['GET'])
def get_profile(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'qualification': user.qualification,
    }), 200

@auth_bp.route('/profile/<int:userid>', methods=['PUT'])

def update_profile(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    data = request.get_json()
    name = data.get('name', '').strip()
    qualification = data.get('qualification', '').strip()

    # Validate at least one field is provided
    if not name and not qualification:
        return jsonify({'message': 'At least one field (name or qualification) is required.'}), 400

    if name:
        user.name = name
    if qualification:
        user.qualification = qualification

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully.'}), 200

@auth_bp.route('/profile/<int:userid>', methods=['DELETE'])

def delete_profile(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Profile deleted successfully.'}), 200

# Route to fetch all data models and their columns
@auth_bp.route('/db/models', methods=['GET'])

def get_all_models():
    from models.models import db
    return jsonify({'database': str(db)}), 200
# Route to delete (drop) all tables in the database
@auth_bp.route('/db', methods=['DELETE'])
def delete_database():
    from models.models import db, User
    # Get the admin user(s) before dropping tables
    admin_users = User.query.filter_by(role='admin').all()
    admin_data = []
    for admin in admin_users:
        admin_data.append({
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'qualification': admin.qualification,
            'role': admin.role
        })
    db.drop_all()
    db.create_all()
    # Re-add admin users
    for admin in admin_data:
        new_admin = User(
            id=admin['id'],
            name=admin['name'],
            email=admin['email'],
            qualification=admin['qualification'],
            role=admin['role']
        )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'All tables dropped and database cleared except admin(s).'}), 200

from models.models import User, Quiz, Subject, Chapter, Question, Result

def model_to_dict(obj):
    result = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        # Convert datetime to isoformat if needed
        if hasattr(val, 'isoformat'):
            val = val.isoformat()
        result[col.name] = val
    return result

# Get all users
@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [model_to_dict(user) for user in users]
    return jsonify({'users': users_data}), 200

# Get all quizzes
@auth_bp.route('/quizzes', methods=['GET'])
def get_all_quizzes():
    quizzes = Quiz.query.all()
    quizzes_data = [model_to_dict(quiz) for quiz in quizzes]
    return jsonify({'quizzes': quizzes_data}), 200

# Get all subjects
@auth_bp.route('/subjects', methods=['GET'])
def get_all_subjects():
    subjects = Subject.query.all()
    subjects_data = [model_to_dict(subject) for subject in subjects]
    return jsonify({'subjects': subjects_data}), 200

# Get all chapters
@auth_bp.route('/chapters', methods=['GET'])
def get_all_chapters():
    chapters = Chapter.query.all()
    chapters_data = [model_to_dict(chapter) for chapter in chapters]
    return jsonify({'chapters': chapters_data}), 200

# Get all questions
@auth_bp.route('/questions', methods=['GET'])
def get_all_questions():
    questions = Question.query.all()
    questions_data = [model_to_dict(question) for question in questions]
    return jsonify({'questions': questions_data}), 200

# Get all results
@auth_bp.route('/results', methods=['GET'])
def get_all_results():
    results = Result.query.all()
    results_data = [model_to_dict(result) for result in results]
    return jsonify({'results': results_data}), 200

