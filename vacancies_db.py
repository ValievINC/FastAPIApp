from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from datetime import datetime


app = FastAPI(
    title="FastAPIApp"
)


class Vacancy(BaseModel):
    name: str
    salary: str
    area_name: str


@app.get("/vacancies/{vacancy_id}")
def get_vacancy(vacancy_id: int):
    connection = sqlite3.connect("vacancies.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM vacancies WHERE id = ?",
        (int(vacancy_id),),
    )
    result = cursor.fetchone()

    if result:
        vacancy = {
            "id": result[0],
            "name": result[1],
            "salary": result[2],
            "area_name": result[3],
            "published_at": result[4]
        }
        return vacancy

    return {"error": "vacancy not found"}


@app.post("/vacancies")
def post_vacancy(vacancy: Vacancy):
    connection = sqlite3.connect("vacancies.db")
    cursor = connection.cursor()

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S%z")

    cursor.execute(
        "INSERT INTO vacancies (name, salary, area_name, published_at) VALUES (?, ?, ?, ?)",
        (vacancy.name, str(vacancy.salary), vacancy.area_name, formatted_date),
    )
    connection.commit()

    cursor.execute("SELECT last_insert_rowid()")
    vacancy_id = cursor.fetchone()[0]

    return {"id": vacancy_id, "name": vacancy.name, "salary": vacancy.salary, "area_name": vacancy.area_name, "published_at": formatted_date}


@app.delete("/vacancies/{vacancy_id}")
def delete_vacancy(vacancy_id: int):
    connection = sqlite3.connect("vacancies.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM vacancies WHERE id = ?",
        (vacancy_id,),
    )
    connection.commit()

    if cursor.rowcount > 0:
        return {"message": "vacancy deleted successfully"}
    else:
        return {"error": "vacancy not found"}