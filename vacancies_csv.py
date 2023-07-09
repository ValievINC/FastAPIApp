from fastapi import FastAPI
import csv
from pydantic import BaseModel
from datetime import datetime


app = FastAPI(
    title="FastAPIApp"
)


class Vacancy(BaseModel):
    name: str
    salary: str
    area_name: str


def read_csv():
    vacancies = []
    with open("vacancies_preprocessed_100.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            vacancy = {
                "id": int(i),
                "name": row["name"],
                "salary": row["salary"],
                "area_name": row["area_name"],
                "published_at": row["published_at"]
            }
            vacancies.append(vacancy)
    return vacancies


def write_csv(vacancies):
    fieldnames = ["id", "name", "salary", "area_name", "published_at"]
    with open("vacancies_preprocessed_100.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for vacancy in vacancies:
            writer.writerow(vacancy)


@app.get("/vacancies/{vacancy_id}")
def get_vacancy(vacancy_id: int):
    vacancies = read_csv()
    for vacancy in vacancies:
        if vacancy.get("id") == vacancy_id:
            return vacancy
    return {"error": "vacancy not found"}


@app.post("/vacancies")
def post_vacancy(vacancy: Vacancy):
    vacancies = read_csv()

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S%z")

    vacancy_data = {
        "id": int(len(vacancies) + 1),
        "name": vacancy.name,
        "salary": str(vacancy.salary),
        "area_name": vacancy.area_name,
        "published_at": formatted_date
    }
    vacancies.append(vacancy_data)

    write_csv(vacancies)

    return {"id": vacancy_data["id"], "name": vacancy.name, "salary": vacancy.salary, "area_name": vacancy.area_name, "published_at": formatted_date}


@app.delete("/vacancies/{vacancy_id}")
def delete_vacancy(vacancy_id: int):
    vacancies = read_csv()

    for vacancy in vacancies:
        if vacancy.get("id") == vacancy_id:
            vacancies.remove(vacancy)
            write_csv(vacancies)
            return {"message": "vacancy deleted successfully"}

    return {"error": "vacancy not found"}