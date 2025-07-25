from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.resultRoutes import result_bp
from routes.questionRoutes import question_bp
from routes.quizRoutes import quiz_bp
from routes.chapterRoutes import chapter_bp
from routes.subjectRoutes import subject_bp
from routes.authRoute import auth_bp
from models.models import db  # your models.py file must contain: db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    # Initialize Extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:5173", "http://localhost:5000", "http://127.0.0.1:5173"], supports_credentials=True)
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(subject_bp, url_prefix='/api/subjects')
    app.register_blueprint(chapter_bp, url_prefix='/api/chapters')
    app.register_blueprint(quiz_bp, url_prefix='/api/quizzes')
    app.register_blueprint(question_bp, url_prefix='/api/questions')
    app.register_blueprint(result_bp, url_prefix='/api/result')

    @app.route('/', methods=['GET'])
    def hello():
        print("hello")
        return "Hello, World!"

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables from models

        # Create an admin user if not exists
        from models.models import User
        from werkzeug.security import generate_password_hash

        admin_email = 'admin@example.com'
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name='Admin',
                email=admin_email,
                password_hash=generate_password_hash('admin123'),
                qualification='Administrator',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
        app.run(debug=True, port=3000)
