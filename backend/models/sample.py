from models import db
from models import User, Subject, Chapter, Quiz, Question, Result, Report, Announcement
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash
from flask import Flask

# --- Ensure all DB operations are run inside an app context ---
def run_with_app_context(func):
    def wrapper(*args, **kwargs):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

# Helper functions
def random_date(start_date, end_date):
    """Generate a random datetime between two dates"""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def create_users():
    """Create sample users"""
    users = [
        User(
            name="Admin User",
            email="admin@quizmaster.com",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            qualification="PhD in Education"
        ),
        User(
            name="Teacher One",
            email="teacher1@quizmaster.com",
            password_hash=generate_password_hash("teacher1"),
            role="admin",
            qualification="MSc in Mathematics"
        )
    ]
    
    # Add regular users
    for i in range(1, 11):
        users.append(User(
            name=f"Student {i}",
            email=f"student{i}@quizmaster.com",
            password_hash=generate_password_hash(f"student{i}"),
            role="user",
            qualification=f"Grade {random.randint(9, 12)}"
        ))
    
    db.session.add_all(users)
    db.session.commit()
    return users

def create_subjects():
    """Create sample subjects"""
    subjects = [
        Subject(name="Mathematics", description="Study of numbers, quantities, and shapes"),
        Subject(name="Science", description="Study of the natural world"),
        Subject(name="History", description="Study of past events"),
        Subject(name="English", description="Study of language and literature"),
        Subject(name="Geography", description="Study of Earth's landscapes")
    ]
    db.session.add_all(subjects)
    db.session.commit()
    return subjects

def create_chapters(subjects):
    """Create sample chapters"""
    chapters = []
    math_chapters = ["Algebra", "Geometry", "Calculus", "Statistics"]
    science_chapters = ["Physics", "Chemistry", "Biology", "Astronomy"]
    history_chapters = ["Ancient History", "Medieval History", "Modern History"]
    english_chapters = ["Grammar", "Literature", "Composition"]
    geography_chapters = ["Physical Geography", "Human Geography", "Environmental Geography"]
    
    for subject in subjects:
        if subject.name == "Mathematics":
            for chap in math_chapters:
                chapters.append(Chapter(name=chap, subject_id=subject.id))
        elif subject.name == "Science":
            for chap in science_chapters:
                chapters.append(Chapter(name=chap, subject_id=subject.id))
        elif subject.name == "History":
            for chap in history_chapters:
                chapters.append(Chapter(name=chap, subject_id=subject.id))
        elif subject.name == "English":
            for chap in english_chapters:
                chapters.append(Chapter(name=chap, subject_id=subject.id))
        elif subject.name == "Geography":
            for chap in geography_chapters:
                chapters.append(Chapter(name=chap, subject_id=subject.id))
    
    db.session.add_all(chapters)
    db.session.commit()
    return chapters

def create_quizzes(chapters):
    """Create sample quizzes"""
    quizzes = []
    for chapter in chapters:
        for i in range(1, 3):  # 2 quizzes per chapter
            quizzes.append(Quiz(
                title=f"{chapter.name} Quiz {i}",
                chapter_id=chapter.id,
                duration=random.randint(300, 1800),  # 5-30 minutes
                created_at=random_date(datetime(2023, 1, 1), datetime.now())
            ))
    
    db.session.add_all(quizzes)
    db.session.commit()
    return quizzes

def create_questions(quizzes):
    """Create sample questions"""
    questions = []
    difficulties = ['easy', 'medium', 'hard']
    options = ['A', 'B', 'C', 'D']
    
    for quiz in quizzes:
        for i in range(1, 6):  # 5 questions per quiz
            questions.append(Question(
                text=f"Sample question {i} about {quiz.title}?",
                option_a=f"Option A for question {i}",
                option_b=f"Option B for question {i}",
                option_c=f"Option C for question {i}",
                option_d=f"Option D for question {i}",
                correct_option=random.choice(options),
                difficulty=random.choice(difficulties),
                quiz_id=quiz.id
            ))
    
    db.session.add_all(questions)
    db.session.commit()
    return questions

def create_results(users, quizzes):
    """Create sample quiz results"""
    results = []
    for user in users[2:]:  # Only students, skip admin and teacher
        for quiz in random.sample(quizzes, random.randint(1, 5)):  # 1-5 quizzes per student
            total_q = random.randint(5, 20)
            attempted = random.randint(3, total_q)
            correct = random.randint(0, attempted)
            score = round((correct / total_q) * 100, 2)
            
            results.append(Result(
                user_id=user.id,
                quiz_id=quiz.id,
                score=score,
                total_questions=total_q,
                attempted_questions=attempted,
                correct_answers=correct,
                time_taken=random.randint(60, 1800),  # 1-30 minutes
                created_at=random_date(datetime(2023, 6, 1), datetime.now())
            ))
    
    db.session.add_all(results)
    db.session.commit()
    return results

def create_reports(users, questions):
    """Create sample question reports"""
    reports = []
    reasons = [
        "Question is unclear",
        "Incorrect answer marked as correct",
        "Typos in question",
        "Options are confusing",
        "Question is too difficult"
    ]
    
    for question in random.sample(questions, 5):  # 5 reported questions
        reports.append(Report(
            user_id=random.choice(users[2:]).id,  # Random student
            quiz_id=question.quiz_id,
            question_id=question.id,
            reason=random.choice(reasons),
            created_at=random_date(datetime(2023, 6, 1), datetime.now())
        ))
    
    db.session.add_all(reports)
    db.session.commit()
    return reports

def create_announcements():
    """Create sample announcements"""
    announcements = [
        Announcement(
            title="System Maintenance",
            message="The system will be down for maintenance on Saturday from 2-4 AM.",
            created_at=datetime(2023, 7, 1)
        ),
        Announcement(
            title="New Quizzes Added",
            message="We've added new quizzes for all subjects. Check them out!",
            created_at=datetime(2023, 7, 15)
        ),
        Announcement(
            title="Upcoming Features",
            message="Leaderboards and achievements coming next month!",
            created_at=datetime(2023, 8, 1)
        )
    ]
    db.session.add_all(announcements)
    db.session.commit()
    return announcements

@run_with_app_context
def main():
    print("Creating sample data...")

    # Clear existing data and create tables
    db.drop_all()
    db.create_all()
    
    # Create all entities
    users = create_users()
    subjects = create_subjects()
    chapters = create_chapters(subjects)
    quizzes = create_quizzes(chapters)
    questions = create_questions(quizzes)
    results = create_results(users, quizzes)
    reports = create_reports(users, questions)
    announcements = create_announcements()
    
    print("Sample data created successfully!")
    print(f"Created: {len(users)} users, {len(subjects)} subjects, {len(chapters)} chapters")
    print(f"Created: {len(quizzes)} quizzes, {len(questions)} questions, {len(results)} results")
    print(f"Created: {len(reports)} reports, {len(announcements)} announcements")

if __name__ == "__main__":
    main()