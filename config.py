"""
Конфигурация приложения с безопасными настройками
"""
import os
from datetime import timedelta


class Config:
    """Базовая конфигурация приложения"""
    
    # Секретный ключ для защиты сессий и CSRF токенов
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    
    # Конфигурация базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки сессий для повышенной безопасности
    SESSION_COOKIE_SECURE = True  # Только HTTPS в продакшене
    SESSION_COOKIE_HTTPONLY = True  # Защита от XSS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Защита от CSRF
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Настройки WTForms CSRF защиты
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Максимальный размер загружаемых файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # HTTP для локальной разработки


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

