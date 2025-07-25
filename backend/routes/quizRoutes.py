from flask import Blueprint, request, jsonify
from models.models import db, Quiz, Chapter, Subject, Question, Report, Result

quiz_bp = Blueprint('quiz', __name__)

# Create a new quiz for a chapter
@quiz_bp.route('/addquiz', methods=['POST'])
def create_quiz():
    data = request.get_json()
    title = data.get('title', '').strip()
    chapter_id = data.get('chapter_id')
    duration = data.get('duration')  # Duration in minutes (should be int or None)

    if not title:
        return jsonify({'message': 'Title is required.'}), 400
    if not chapter_id:
        return jsonify({'message': 'Chapter ID is required.'}), 400

    # Ensure chapter exists
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({'message': 'Chapter not found.'}), 404

    # Store duration as integer minutes if provided, else None
    quiz = Quiz(title=title, chapter_id=chapter_id, duration=int(duration) if duration is not None else None)
    db.session.add(quiz)
    db.session.commit()
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'chapter_id': quiz.chapter_id,
        'duration': quiz.duration,  # duration in minutes
        'created_at': quiz.created_at.isoformat() if quiz.created_at else None
    }), 201

# Get all quizzes
@quiz_bp.route('/', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    result = []
    for q in quizzes:
        result.append({
            'id': q.id,
            'title': q.title,
            'chapter_id': q.chapter_id,
            'duration': q.duration,  # duration in minutes
            'created_at': q.created_at.isoformat() if q.created_at else None
        })
    return jsonify(result), 200

# Get all quizzes for a chapter
@quiz_bp.route('/chapter/<int:chapter_id>', methods=['GET'])
def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    result = []
    for q in quizzes:
        result.append({
            'id': q.id,
            'title': q.title,
            'chapter_id': q.chapter_id,
            'duration': q.duration,  # duration in minutes
            'created_at': q.created_at.isoformat() if q.created_at else None
        })
    return jsonify(result), 200

# Get all quizzes for a subject (across all its chapters)
@quiz_bp.route('/subject/<int:subject_id>', methods=['GET'])
def get_quizzes_by_subject(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_ids = [ch.id for ch in chapters]
    quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).all() if chapter_ids else []
    result = []
    for q in quizzes:
        result.append({
            'id': q.id,
            'title': q.title,
            'chapter_id': q.chapter_id,
            'duration': q.duration,  # duration in minutes
            'created_at': q.created_at.isoformat() if q.created_at else None
        })
    return jsonify(result), 200

# Get a single quiz by id
@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404
    chapter = Chapter.query.get(quiz.chapter_id) if quiz.chapter_id else None
    subject = Subject.query.get(chapter.subject_id) if chapter and chapter.subject_id else None
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'chapter_id': quiz.chapter_id,
        'duration': quiz.duration,  # duration in minutes
        'chapter_name': chapter.name if chapter else None,
        'subject_id': chapter.subject_id if chapter else None,
        'subject_name': subject.name if subject else None,
        'created_at': quiz.created_at.isoformat() if quiz.created_at else None
    }), 200

# Update quiz name and duration
@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404
    data = request.get_json()
    title = data.get('title', '').strip()
    duration = data.get('duration')
    if not title:
        return jsonify({'message': 'Title is required.'}), 400
    quiz.title = title
    if duration is not None:
        try:
            quiz.duration = int(duration)  # duration in minutes
        except (ValueError, TypeError):
            return jsonify({'message': 'Duration must be an integer.'}), 400
    db.session.commit()
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'duration': getattr(quiz, 'duration', None),  # duration in minutes
        'chapter_id': quiz.chapter_id,
        'created_at': quiz.created_at.isoformat() if quiz.created_at else None
    }), 200

# Delete a quiz
@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz deleted.'}), 200

# API to get quiz questions for taking a quiz (no correct option sent)
@quiz_bp.route('/<int:quiz_id>/take', methods=['GET'])
def get_quiz_questions_for_take(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    result = []
    for q in questions:
        # Use correct attribute names for options
        result.append({
            'id': q.id,
            'text': q.text,
            'options': [
                getattr(q, 'option_a', None),
                getattr(q, 'option_b', None),
                getattr(q, 'option_c', None),
                getattr(q, 'option_d', None)
            ],
            'image': getattr(q, 'image', None)
        })
    return jsonify({'quiz_id': quiz_id, 'duration': quiz.duration, 'questions': result}), 200  # duration in minutes

# API to submit quiz answers and report questions
@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz_answers(quiz_id):
    data = request.get_json()
    answers = data.get('answers')  # dict: {question_id: selected_option_index or -1}
    user_id = data.get('user_id')  # Optionally get user_id if sent

    if not isinstance(answers, dict):
        return jsonify({"message": "answers dict required."}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404

    # Get all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)

    attempted_questions = 0
    correct_answers = 0
    user_correct_answers = {}
    result_answers = {}

    for question in questions:
        qid_str = str(question.id)
        selected = answers.get(qid_str, None)
        if selected is None:
            user_correct_answers[qid_str] = False
            continue
        if selected == -1:
            # Optionally handle reported question here if needed
            user_correct_answers[qid_str] = False
            result_answers[qid_str] = -1
            continue
        attempted_questions += 1

        # Convert correct_option ('A', 'B', 'C', 'D') to index (0-3)
        correct_index = ord(question.correct_option.upper()) - ord('A')
        is_correct = (selected == correct_index)
        if is_correct:
            correct_answers += 1
        user_correct_answers[qid_str] = is_correct
        result_answers[qid_str] = selected

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0.0

    # Get quiz, chapter, and subject info for return
    chapter = Chapter.query.get(quiz.chapter_id) if quiz.chapter_id else None
    subject = Subject.query.get(chapter.subject_id) if chapter and chapter.subject_id else None

    # Get time_taken, ensure it's int (required by model)
    time_taken = data.get('time_taken', None)
    try:
        time_taken = int(time_taken)  # time_taken in minutes
    except (TypeError, ValueError):
        time_taken = 0

    # Save or update result in the Result model
    from models.models import Result
    if user_id is not None:
        # Check if a result already exists for this user and quiz
        result_obj = Result.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        if result_obj:
            # Update existing result
            result_obj.score = score
            result_obj.total_questions = total_questions
            result_obj.attempted_questions = attempted_questions
            result_obj.correct_answers = correct_answers
            result_obj.time_taken = time_taken  # time_taken in minutes
        else:
            # Add new result
            result_obj = Result(
                user_id=user_id,
                quiz_id=quiz_id,
                score=score,
                total_questions=total_questions,
                attempted_questions=attempted_questions,
                correct_answers=correct_answers,
                time_taken=time_taken  # time_taken in minutes
            )
            db.session.add(result_obj)
        db.session.commit()

    return jsonify({
        "score": score,  # Percentage score (0-100)
        "total_questions": total_questions,
        "attempted_questions": attempted_questions,
        "correct_answers": correct_answers,
        "time_taken": time_taken,  # time_taken in minutes
        "user_correct_answers": user_correct_answers,  # Dict mapping question_id to boolean
        "user_id": user_id,
        "answers": result_answers,  # Dict mapping question_id to selected option index
        "quiz": {
            "id": quiz.id,
            "title": quiz.title,
            "chapter_id": quiz.chapter_id,
            "duration": quiz.duration,  # duration in minutes
            "chapter_name": chapter.name if chapter else None,
            "subject_id": chapter.subject_id if chapter else None,
            "subject_name": subject.name if subject else None,
            "created_at": quiz.created_at.isoformat() if quiz.created_at else None
        }
    }), 200
