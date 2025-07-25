from flask import Blueprint, jsonify
from models.models import db, Result

result_bp = Blueprint('result', __name__)

@result_bp.route('/<int:user_id>', methods=['GET'])
def get_results_by_user(user_id):
    results = Result.query.filter_by(user_id=user_id).all()
    result_list = []
    for r in results:
        result_list.append({
            'id': r.id,
            'user_id': r.user_id,
            'quiz_id': r.quiz_id,
            'score': r.score,
            'total_questions': r.total_questions,
            'attempted_questions': r.attempted_questions,
            'correct_answers': r.correct_answers,
            'created_at': r.created_at.isoformat() if r.created_at else None
        })
    return jsonify(result_list), 200
