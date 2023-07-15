# Установка базового образа Python
FROM python:3.9

# Установка переменной окружения для отключения вывода буферизации Python
ENV PYTHONUNBUFFERED=1

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование зависимостей проекта
COPY poetry.lock pyproject.toml /app/

# Установка зависимостей с помощью Poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копирование файлов проекта в контейнер
COPY . /app

# Запуск приложения
CMD ["python", "main.py"]
