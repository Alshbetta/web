"""
Главное приложение Flask с безопасной аутентификацией
"""
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from models import db, User
from forms import RegistrationForm, LoginForm
from config import config


def create_app(config_name='development'):
    """
    Фабрика приложений Flask
    
    Args:
        config_name (str): Имя конфигурации (development/production)
    
    Returns:
        Flask: Настроенное приложение
    """
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(config[config_name])
    
    # Инициализация расширений
    db.init_app(app)
    
    # Настройка Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Загрузка пользователя по ID"""
        return User.query.get(int(user_id))
    
    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()
    
    # ========== МАРШРУТЫ ==========
    
    @app.route('/')
    def index():
        """Главная страница"""
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Регистрация нового пользователя"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        
        if form.validate_on_submit():
            # Создание нового пользователя
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            try:
                db.session.add(user)
                db.session.commit()
                
                flash('Регистрация успешна! Теперь вы можете войти.', 'success')
                return redirect(url_for('login'))
            
            except Exception as e:
                db.session.rollback()
                flash('Произошла ошибка при регистрации. Попробуйте снова.', 'danger')
                app.logger.error(f'Registration error: {e}')
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Вход пользователя"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            # Поиск пользователя по имени или email
            user = User.query.filter(
                (User.username == form.username.data) |
                (User.email == form.username.data)
            ).first()
            
            # Проверка пользователя и пароля
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('Ваш аккаунт деактивирован.', 'warning')
                    return redirect(url_for('login'))
                
                # Вход пользователя
                login_user(user, remember=form.remember_me.data)
                user.update_last_login()
                
                flash(f'Добро пожаловать, {user.username}!', 'success')
                
                # Перенаправление на запрошенную страницу или dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            
            else:
                flash('Неверное имя пользователя или пароль.', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """Выход пользователя"""
        logout_user()
        flash('Вы вышли из системы.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Личный кабинет пользователя"""
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/profile')
    @login_required
    def profile():
        """Профиль пользователя"""
        return render_template('profile.html', user=current_user)
    
    # ========== ОБРАБОТЧИКИ ОШИБОК ==========
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Обработка ошибки 404"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Обработка ошибки 500"""
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # ========== КОНТЕКСТНЫЕ ПРОЦЕССОРЫ ==========
    
    @app.context_processor
    def inject_year():
        """Добавление текущего года в контекст шаблонов"""
        from datetime import datetime
        return {'current_year': datetime.now().year}
    
    return app


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000)

