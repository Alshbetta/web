#!/usr/bin/env python3
"""
Скрипт проверки установки и конфигурации
"""
import sys
import os


def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - требуется 3.8+")
        return False


def check_dependencies():
    """Проверка установленных зависимостей"""
    print("\n📦 Проверка зависимостей...")
    
    dependencies = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'werkzeug',
        'email_validator',
        'dotenv',
        'cryptography'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - не установлен")
            all_ok = False
    
    return all_ok


def check_files():
    """Проверка наличия необходимых файлов"""
    print("\n📄 Проверка файлов проекта...")
    
    required_files = [
        'app.py',
        'models.py',
        'forms.py',
        'config.py',
        'run.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'static/css/style.css'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - не найден")
            all_ok = False
    
    return all_ok


def check_env():
    """Проверка файла .env"""
    print("\n🔐 Проверка конфигурации...")
    
    if os.path.exists('.env'):
        print("   ✅ Файл .env существует")
        
        # Проверка наличия ключей
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'SECRET_KEY' in content:
            print("   ✅ SECRET_KEY настроен")
        else:
            print("   ⚠️  SECRET_KEY не найден в .env")
            
        if 'DATABASE_URL' in content:
            print("   ✅ DATABASE_URL настроен")
        else:
            print("   ⚠️  DATABASE_URL не найден в .env")
            
        return True
    else:
        print("   ⚠️  Файл .env не найден (будет создан при запуске)")
        return True


def check_app():
    """Проверка возможности импорта приложения"""
    print("\n🚀 Проверка приложения...")
    
    try:
        from app import create_app
        print("   ✅ Приложение импортируется корректно")
        
        try:
            app = create_app('development')
            print("   ✅ Приложение создается успешно")
            return True
        except Exception as e:
            print(f"   ❌ Ошибка создания приложения: {e}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False


def main():
    """Главная функция"""
    print("=" * 60)
    print("🔍 Проверка установки SecureApp")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_files(),
        check_env(),
        check_app()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("✅ Все проверки пройдены успешно!")
        print("=" * 60)
        print("\n🚀 Готово к запуску!")
        print("\nДля запуска выполните:")
        print("  python run.py")
        print("\nили:")
        print("  ./start.sh")
        return 0
    else:
        print("❌ Обнаружены проблемы")
        print("=" * 60)
        print("\n📝 Рекомендации:")
        print("1. Запустите: ./setup.sh")
        print("2. Или установите зависимости: pip install -r requirements.txt")
        print("3. Смотрите QUICKSTART.md для подробных инструкций")
        return 1


if __name__ == '__main__':
    exit(main())

