from flask import Blueprint, request, jsonify
from models.models import db, Subject
from flask_jwt_extended import jwt_required, get_jwt_identity

subject_bp = Blueprint('subject', __name__)

# Create a new subject
@subject_bp.route('/addsubject', methods=['POST'])
# @jwt_required()  # Temporarily disabled for testing
def create_subject():
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    if not name:
        return jsonify({'message': 'Subject name is required.'}), 400
    if Subject.query.filter_by(name=name).first():
        return jsonify({'message': 'Subject already exists.'}), 409
    subject = Subject(name=name, description=description)
    db.session.add(subject)
    db.session.commit()
    return jsonify({'id': subject.id, 'name': subject.name, 'description': subject.description}), 201

# Update a subject
@subject_bp.route('/<int:subject_id>', methods=['PUT'])
# @jwt_required()
def update_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found.'}), 404
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    if not name:
        return jsonify({'message': 'Subject name is required.'}), 400
    if Subject.query.filter(Subject.name == name, Subject.id != subject_id).first():
        return jsonify({'message': 'Another subject with this name already exists.'}), 409
    subject.name = name
    subject.description = description
    db.session.commit()
    return jsonify({'id': subject.id, 'name': subject.name, 'description': subject.description}), 200

# Delete a subject
@subject_bp.route('/<int:subject_id>', methods=['DELETE'])
# @jwt_required()
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found.'}), 404
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully.'}), 200

# Get all subjects with their chapters and quizzes
@subject_bp.route('/with-details', methods=['GET'])
# @jwt_required()  # Temporarily disabled for testing
def get_subjects_with_details():
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        chapters = []
        for chapter in subject.chapters:
            quizzes = []
            for quiz in chapter.quizzes:
                print(quiz)
                quizzes.append({
                    'id': quiz.id,
                    'title': quiz.title,
                    'duration' : quiz.duration
                    })
            chapters.append({
                'id': chapter.id,
                'name': chapter.name,
                'quizzes': quizzes
            })
        result.append({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'chapters': chapters
        })
    return jsonify(result), 200

@subject_bp.route('/<int:subject_id>', methods=['GET'])
# @jwt_required()
def get_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found.'}), 404
    chapters = []
    for chapter in subject.chapters:
        quizzes = []
        for quiz in chapter.quizzes:
            quizzes.append({
                'id': quiz.id,
                'title': quiz.title
            })
        chapters.append({
            'id': chapter.id,
            'name': chapter.name,
            'quizzes': quizzes
        })
    return jsonify({
        'id': subject.id,
        'name': subject.name,
        'description': subject.description,
        'chapters': chapters
    }), 200
