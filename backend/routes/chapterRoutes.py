from flask import Blueprint, request, jsonify
from models.models import db, Chapter, Subject
from flask_jwt_extended import jwt_required

chapter_bp = Blueprint('chapter', __name__)

# Create a new chapter
@chapter_bp.route('/addchapter', methods=['POST'])
# @jwt_required()  # Uncomment to require authentication
def create_chapter():
    data = request.get_json()
    name = data.get('name', '').strip()
    subject_id = data.get('subject_id')
    if not name or not subject_id:
        return jsonify({'message': 'Chapter name and subject_id are required.'}), 400
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found.'}), 404
    if Chapter.query.filter_by(name=name, subject_id=subject_id).first():
        return jsonify({'message': 'Chapter already exists for this subject.'}), 409
    chapter = Chapter(name=name, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()
    return jsonify({'id': chapter.id, 'name': chapter.name, 'subject_id': chapter.subject_id}), 201

# Get all chapters of a subject
@chapter_bp.route('/subject/<int:subject_id>', methods=['GET'])
# @jwt_required()
def get_chapters_by_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'message': 'Subject not found.'}), 404
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    result = [{
        'id': c.id,
        'name': c.name,
        'subject_id': c.subject_id,
        'subject_name': subject.name
    } for c in chapters]
    print(result)
    return jsonify(result), 200

# Update a chapter
@chapter_bp.route('/<int:chapter_id>', methods=['PUT'])
# @jwt_required()
def update_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({'message': 'Chapter not found.'}), 404
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'message': 'Chapter name is required.'}), 400
    # Prevent duplicate chapter name in the same subject
    if Chapter.query.filter(Chapter.name == name, Chapter.subject_id == chapter.subject_id, Chapter.id != chapter_id).first():
        return jsonify({'message': 'Another chapter with this name already exists in this subject.'}), 409
    chapter.name = name
    db.session.commit()
    return jsonify({'id': chapter.id, 'name': chapter.name, 'subject_id': chapter.subject_id}), 200

# Delete a chapter
@chapter_bp.route('/<int:chapter_id>', methods=['DELETE'])
# @jwt_required()
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({'message': 'Chapter not found.'}), 404
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({'message': 'Chapter deleted successfully.'}), 200
# Get info about a particular chapter
@chapter_bp.route('/<int:chapter_id>', methods=['GET'])
# @jwt_required()
def get_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({'message': 'Chapter not found.'}), 404
    subject = Subject.query.get(chapter.subject_id) if chapter.subject_id else None
    return jsonify({
        'id': chapter.id,
        'name': chapter.name,
        'subject_id': chapter.subject_id,
        'subject_name': subject.name if subject else None
    }), 200