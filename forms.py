"""
Формы с валидацией и CSRF защитой
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError, Regexp
)
from models import User


class RegistrationForm(FlaskForm):
    """Форма регистрации с валидацией"""
    
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(message='Это поле обязательно'),
            Length(min=3, max=80, message='Имя должно быть от 3 до 80 символов'),
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message='Только латинские буквы, цифры, дефис и подчеркивание'
            )
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Это поле обязательно'),
            Email(message='Неверный формат email')
        ]
    )
    
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Это поле обязательно'),
            Length(min=8, message='Пароль должен быть минимум 8 символов'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                message='Пароль должен содержать заглавные и строчные буквы, цифры'
            )
        ]
    )
    
    password_confirm = PasswordField(
        'Подтвердите пароль',
        validators=[
            DataRequired(message='Это поле обязательно'),
            EqualTo('password', message='Пароли должны совпадать')
        ]
    )
    
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, field):
        """Проверка уникальности имени пользователя"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Это имя пользователя уже занято')
    
    def validate_email(self, field):
        """Проверка уникальности email"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Этот email уже зарегистрирован')


class LoginForm(FlaskForm):
    """Форма входа"""
    
    username = StringField(
        'Имя пользователя или Email',
        validators=[DataRequired(message='Это поле обязательно')]
    )
    
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(message='Это поле обязательно')]
    )
    
    remember_me = BooleanField('Запомнить меня')
    
    submit = SubmitField('Войти')

