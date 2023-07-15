from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse

from database import create_table, create_connection
from auth import generate_token, generate_expiration

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

create_table()


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


# Страница авторизации пользователя
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Страница получения информации о зарплате
@app.get("/salary", response_class=HTMLResponse)
async def salary(request: Request):
    return templates.TemplateResponse("salary.html", {"request": request})


# Обработка после авторизации
@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    connection = create_connection()
    try:
        cursor = connection.cursor()
        select_employee_query = f"SELECT id FROM employees WHERE login = '{username}' AND password = '{password}'"
        cursor.execute(select_employee_query)
        result = cursor.fetchone()
        if result:
            token = generate_token()
            expiration = generate_expiration()
            update_token_query = f"UPDATE employees SET token = '{token}', token_expiration = '{expiration}' WHERE login = '{username}'"
            cursor.execute(update_token_query)
            connection.commit()
            return RedirectResponse(url='/token?token={}&token_expiration={}'.format(token, expiration))
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        print(f"Error logging in: {e}")
        raise HTTPException(status_code=401, detail="Invalid username or password, please try again")
    finally:
        if connection:
            cursor.close()
            connection.close()


# Обработка токена и вывод пользователю
@app.post("/token", response_class=HTMLResponse)
async def token_post(request: Request, token: str = Query(...), token_expiration: str = Query(...)):
    return templates.TemplateResponse("token.html",
                                      {"request": request, "token": token, "token_expiration": token_expiration})


# Получение персональной информации по токену
@app.post('/salary', response_class=HTMLResponse)
def get_salary(request: Request, token: str = Form(...)):
    connection = create_connection()
    try:
        cursor = connection.cursor()
        select_login_query = f"SELECT login, token_expiration FROM employees WHERE token = '{token}'"
        cursor.execute(select_login_query)
        result = cursor.fetchone()
        if result:
            login = result[0]
            token_expiration = result[1]
            if token_expiration >= datetime.now():
                select_salary_query = f"SELECT salary, next_raise_date FROM employees WHERE login = '{login}'"
                cursor.execute(select_salary_query)
                result = cursor.fetchone()
                if result:
                    salary = result[0]
                    next_raise_date = result[1].strftime('%Y-%m-%d')
                    return RedirectResponse(
                        url='/personal_data?salary={}&next_raise_date={}'.format(salary, next_raise_date))
            else:
                raise HTTPException(status_code=401, detail='Token expired')
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        print(f"Error retrieving salary: {e}")
        raise HTTPException(status_code=401, detail='Invalid token')
    finally:
        if connection:
            cursor.close()
            connection.close()


# Обработка персональной информации и вывод пользователю
@app.post("/personal_data", response_class=HTMLResponse)
async def personal_data_post(request: Request, salary: str = Query(...), next_raise_date: str = Query(...)):
    return templates.TemplateResponse("personal_data.html",
                                      {"request": request, "salary": salary, "next_raise_date": next_raise_date})


# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("error.html",
                                      {"request": request, "status_code": exc.status_code, "message": exc.detail},
                                      status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
