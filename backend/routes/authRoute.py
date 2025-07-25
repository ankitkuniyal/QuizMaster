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
    password = data.get('password', '')

    # Validate at least one field is provided
    if not name and not qualification and not password:
        return jsonify({'message': 'At least one field (name, qualification, or password) is required.'}), 400

    if name:
        user.name = name
    if qualification:
        user.qualification = qualification
    if password:
        if len(password) < 8:
            return jsonify({'message': 'Password must be at least 8 characters long.'}), 400
        user.password_hash = generate_password_hash(password)

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
    db.drop_all()
    db.create_all()
    # Re-add admin users
    new_admin = User(
            name='Admin',
                email="admin@example.com",
                password_hash=generate_password_hash('admin123'),
                qualification='Administrator',
                role='admin'
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

# leagues.py (Constants)
LEAGUES = [
    {"name": "Rookie", "min_score": 0, "icon": "fa-seedling", "color": "#4ade80"},      # Soft green
    {"name": "Bronze", "min_score": 50, "icon": "fa-medal", "color": "#cd7f32"},        # Bronze
    {"name": "Silver", "min_score": 65, "icon": "fa-medal", "color": "#a5a5a5"},        # Deeper silver
    {"name": "Gold", "min_score": 80, "icon": "fa-medal", "color": "#ffd700"},          # Gold
    {"name": "Platinum", "min_score": 90, "icon": "fa-crown", "color": "#38bdf8"}       # Vibrant blue
]
# authRoute.py
@auth_bp.route('/league', methods=['POST'])
def calculate_league():
    data = request.get_json()
    # Required params
    avg_score = float(data.get('avg_score', 0))
    streak = int(data.get('streak', 0))
    quizzes_submitted = int(data.get('quizzes_submitted', 0))
    
    # Edge case: No quizzes taken
    if quizzes_submitted == 0:
        return jsonify({
            "league": LEAGUES[0],
            "next_league": LEAGUES[1],
            "progress": 0,
            "streak_boost": False
        })
    
    # Calculate league score (custom formula)
    league_score = calculate_league_score(avg_score, streak,quizzes_submitted)
    
    # Determine league
    current_league = LEAGUES[0]
    next_league = None
    streak_boost = False
    
    for i, league in enumerate(LEAGUES):
        if league_score >= league['min_score']:
            current_league = league
            if i < len(LEAGUES) - 1:
                next_league = LEAGUES[i + 1]
    
    # Streak boost - temporary 1-tier promotion
    if streak >= 7 and current_league != LEAGUES[-1]:
        current_league = LEAGUES[min(i + 1, len(LEAGUES)-1)]
        streak_boost = True
    
    # Progress to next league (0-100)
    progress = 0
    if next_league:
        progress = min(100, 
            ((league_score - current_league['min_score']) / 
             (next_league['min_score'] - current_league['min_score'])) * 100
        )
    
    return jsonify({
        "league": current_league,
        "next_league": next_league,
        "progress": round(progress),
        "streak_boost": streak_boost,
        "league_score": league_score  
    })

def calculate_league_score(avg_score, streak, quizzes_submitted):
    # League score formula: 70% avg_score, 20% quizzes_submitted (log scale), 10% streak
    league_score = (
        (avg_score * 0.7) +
        (min(100, quizzes_submitted) ** 0.5 * 10 * 0.2) +  # sqrt scale, max 100 quizzes
        (min(streak, 30) * 2 * 0.1)  # streak capped at 30, scaled to 60
    )
    return league_score