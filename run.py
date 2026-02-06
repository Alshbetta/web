#!/usr/bin/env python3
"""
Скрипт запуска приложения
"""
import os
import secrets
from app import create_app


def generate_secret_key():
    """Генерация секретного ключа если он не установлен"""
    if not os.environ.get('SECRET_KEY'):
        key = secrets.token_hex(32)
        print("=" * 60)
        print("⚠️  ВАЖНО: SECRET_KEY не установлен!")
        print("=" * 60)
        print("\nСоздайте файл .env со следующим содержимым:\n")
        print(f"SECRET_KEY={key}")
        print("DATABASE_URL=sqlite:///users.db")
        print("FLASK_ENV=development")
        print("FLASK_DEBUG=True")
        print("\n" + "=" * 60)
        
        # Устанавливаем временный ключ для разработки
        os.environ['SECRET_KEY'] = key


if __name__ == '__main__':
    generate_secret_key()
    
    # Определение окружения
    env = os.getenv('FLASK_ENV', 'development')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Создание приложения
    app = create_app(env)
    
    print("\n" + "=" * 60)
    print("🚀 Запуск SecureApp")
    print("=" * 60)
    print(f"Окружение: {env}")
    print(f"Debug режим: {debug}")
    print(f"URL: http://localhost:5000")
    print("=" * 60 + "\n")
    
    # Запуск сервера
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug
    )

