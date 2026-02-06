"""
Модели базы данных с безопасным хранением паролей
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Модель пользователя с безопасным хранением учетных данных
    
    Использует:
    - Werkzeug для хеширования паролей (PBKDF2-SHA256)
    - Flask-Login для управления сессиями
    - Автоматическое отслеживание времени создания
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def set_password(self, password):
        """
        Безопасное хеширование пароля с использованием PBKDF2-SHA256
        
        Args:
            password (str): Пароль в открытом виде
        """
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )
    
    def check_password(self, password):
        """
        Проверка пароля с использованием безопасного сравнения
        
        Args:
            password (str): Пароль для проверки
            
        Returns:
            bool: True если пароль совпадает
        """
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Обновление времени последнего входа"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """
        Безопасное представление пользователя (без пароля)
        
        Returns:
            dict: Данные пользователя
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

