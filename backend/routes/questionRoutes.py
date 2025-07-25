from flask import Blueprint, request, jsonify
from models.models import db, Question

question_bp = Blueprint('questions', __name__)

# Get all questions for a quiz
@question_bp.route('/quiz/<int:quiz_id>', methods=['GET'])
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    result = []
    for q in questions:
        result.append({
            'id': q.id,
            'text': q.text,
            'options': [
                {'text': q.option_a},
                {'text': q.option_b},
                {'text': q.option_c},
                {'text': q.option_d}
            ],
            'correctIndex': ord(q.correct_option.upper()) - ord('A'),
            'difficulty': q.difficulty
        })
    return jsonify(result), 200

# Get a single question
@question_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    q = Question.query.get_or_404(question_id)
    return jsonify({
        'id': q.id,
        'text': q.text,
        'options': [
            {'text': q.option_a},
            {'text': q.option_b},
            {'text': q.option_c},
            {'text': q.option_d}
        ],
        'correctIndex': ord(q.correct_option.upper()) - ord('A'),
        'difficulty': q.difficulty
    }), 200

# Create a new question
@question_bp.route('/<int:quiz_id>', methods=['POST'])
def create_question(quiz_id):
    data = request.json
    options = data.get('options', [])
    if len(options) != 4:
        return jsonify({'error': 'Exactly 4 options required'}), 400
    correct_index = data.get('correctIndex', 0)
    if not (0 <= correct_index <= 3):
        return jsonify({'error': 'correctIndex must be 0-3'}), 400
    q = Question(
        text=data.get('text', ''),
        option_a=options[0].get('text', ''),
        option_b=options[1].get('text', ''),
        option_c=options[2].get('text', ''),
        option_d=options[3].get('text', ''),
        correct_option=chr(ord('A') + correct_index),
        quiz_id=quiz_id,
        difficulty=data.get('difficulty', 'easy'),
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({'id': q.id}), 201

# Update a question
@question_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    q = Question.query.get_or_404(question_id)
    data = request.json
    q.text = data.get('text', q.text)
    options = data.get('options', [])
    if len(options) == 4:
        q.option_a = options[0].get('text', q.option_a)
        q.option_b = options[1].get('text', q.option_b)
        q.option_c = options[2].get('text', q.option_c)
        q.option_d = options[3].get('text', q.option_d)
    correct_index = data.get('correctIndex')
    if correct_index is not None and 0 <= correct_index <= 3:
        q.correct_option = chr(ord('A') + correct_index)
    if 'difficulty' in data:
        q.difficulty = data['difficulty']
    db.session.commit()
    return jsonify({'message': 'Question updated'}), 200

# Delete a question
@question_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    db.session.delete(q)
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200
