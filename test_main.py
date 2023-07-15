import pytest
import uvicorn
from fastapi.testclient import TestClient

from main import app, create_table, create_connection
from database import insert_employee


@pytest.fixture(scope="module")
def test_app():
    # Создаем тестового клиента для FastAPI
    client = TestClient(app)

    # Создаем таблицу в тестовой базе данных
    create_table()

    # Вставляем тестовых пользователей в базу данных
    connection = create_connection()
    try:
        cursor = connection.cursor()
        for i in range(1, 11):
            insert_employee(cursor, f"User{i}", f"password{i}", 50000, "2023-12-31")
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()

    # Возвращаем тестовый клиент для использования в тестах
    yield client


# Функция извлечения токена
def extract_token(response_text):
    token_start_index = response_text.index("Token: ") + len("Token: ")
    token_end_index = response_text.index("<", token_start_index)
    token = response_text[token_start_index:token_end_index].strip()
    return token


def test_home(test_app):
    # Тестирование главной страницы
    response = test_app.get("/")
    assert response.status_code == 200
    assert "Welcome to the Salary Service" in response.text
    assert "Login" in response.text
    assert "Salary" in response.text


def test_login(test_app):
    # Тестирование страницы авторизации
    response = test_app.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text


def test_invalid_login(test_app):
    # Тестирование неверной авторизации
    response = test_app.post("/login", data={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert "Invalid username or password, please try again" in response.text


def test_valid_login(test_app):
    # Тестирование успешной авторизации
    response = test_app.post("/login", data={"username": "User1", "password": "password1"})
    assert response.status_code == 200
    assert "Token: " in response.text
    assert "Expiration: " in response.text


def test_token(test_app):
    # Тестирование страницы токена
    response = test_app.post("/token?token=abc123&token_expiration=2022-01-01")
    assert response.status_code == 200
    assert "Your Token" in response.text
    assert "Token: abc123" in response.text
    assert "Expiration: 2022-01-01" in response.text


def test_salary(test_app):
    # Тестирование страницы получения информации о зарплате
    response = test_app.get("/salary")
    assert response.status_code == 200
    assert "Salary" in response.text


def test_invalid_token(test_app):
    # Тестирование запроса информации о зарплате с неверным токеном
    response = test_app.post("/salary", data={"token": "invalid_token"})
    assert response.status_code == 401
    assert "Invalid token" in response.text


def test_valid_token(test_app):
    # Тестирование успешной авторизации
    login_response = test_app.post("/login", data={"username": "User1", "password": "password1"})
    assert login_response.status_code == 200
    assert "Token: " in login_response.text
    assert "Expiration: " in login_response.text

    # Извлечение токена из текста ответа
    token = extract_token(login_response.text)
    print("Extracted token:", token)

    # Запрос информации о зарплате с использованием скопированного токена
    salary_response = test_app.post("/salary", data={"token": token})
    assert salary_response.status_code == 200
    assert "Your Personal Data" in salary_response.text
    assert "Salary: 50000" in salary_response.text
    assert "Next raise date: 2023-12-31" in salary_response.text


def test_personal_data(test_app):
    # Тестирование страницы персональных данных
    response = test_app.post("/personal_data?salary=5000&next_raise_date=2022-12-31")
    assert response.status_code == 200
    assert "Your Personal Data" in response.text
    assert "Salary: 5000" in response.text
    assert "Next raise date: 2022-12-31" in response.text


# Запуск сервера для выполнения тестов
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
