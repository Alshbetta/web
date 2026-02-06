#!/bin/bash
# Скрипт быстрого запуска приложения

echo "🚀 Запуск SecureApp..."

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено."
    echo "Запустите: ./setup.sh"
    exit 1
fi

# Активация виртуального окружения
source venv/bin/activate

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Создание с настройками по умолчанию..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///users.db
FLASK_ENV=development
FLASK_DEBUG=True
EOF
    echo "✅ Файл .env создан"
fi

# Загрузка переменных окружения
export $(cat .env | xargs)

# Запуск приложения
python run.py

