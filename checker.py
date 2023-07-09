import subprocess
import requests
import time

app_process = subprocess.Popen(["uvicorn", "vacancies_db:app", "--reload", ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# Testing GET
response = requests.get("http://127.0.0.1:8000/vacancies/1")
data = str(response.json())
original_data = "{'id': 1, 'name': 'Software Engineer for Windows applications, COM-components development', 'salary': '', 'area_name': 'Москва', 'published_at': '2003-10-07T00:00:00+0400'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[GET] Данные с запроса не соответствуют ожидаемым данным'})
    exit()

response = requests.get("http://127.0.0.1:8000/vacancies/100")
data = str(response.json())
original_data = "{'id': 100, 'name': 'Senior CAD Engineer   (Job# 253952)', 'salary': '', 'area_name': 'Москва', 'published_at': '2003-07-17T20:03:13+0400'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[GET] Данные с запроса не соответствуют ожидаемым данным'})
    exit()

response = requests.get("http://127.0.0.1:8000/vacancies/228")
data = str(response.json())
original_data = "{'error': 'vacancy not found'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[GET] Данные с запроса не соответствуют ожидаемым данным'})
    exit()


# Testing POST
vacancy = {
    "name": "Test",
    "salary": "100000",
    "area_name": "Ufa"
}

response = requests.post("http://127.0.0.1:8000/vacancies", json=vacancy, verify=False)
get_response = requests.get("http://127.0.0.1:8000/vacancies/101")
data = str(get_response.json())
original_data = "{'id': 101, 'name': 'Test', 'salary': '100000', 'area_name': 'Ufa', 'published_at':"
if original_data not in data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[POST] Данные с запроса не соответствуют ожидаемым данным'})
    exit()


vacancy = {
    "name": "Blah-blah-blah",
    "salary": "",
    "area_name": "New York"
}

response = requests.post("http://127.0.0.1:8000/vacancies", json=vacancy, verify=False)
get_response = requests.get("http://127.0.0.1:8000/vacancies/102")
data = str(get_response.json())
original_data = "{'id': 102, 'name': 'Blah-blah-blah', 'salary': '', 'area_name': 'New York', 'published_at':"
if original_data not in data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[POST] Данные с запроса не соответствуют ожидаемым данным'})
    exit()


# Testing DELETE
response = requests.delete("http://127.0.0.1:8000/vacancies/102", json=vacancy, verify=False)
get_response = requests.get("http://127.0.0.1:8000/vacancies/102")
data = str(get_response.json())
original_data = "{'error': 'vacancy not found'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[DELETE] Данные с запроса не соответствуют ожидаемым данным'})
    exit()

response = requests.delete("http://127.0.0.1:8000/vacancies/101", json=vacancy, verify=False)
get_response = requests.get("http://127.0.0.1:8000/vacancies/101")
data = str(get_response.json())
original_data = "{'error': 'vacancy not found'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[DELETE] Данные с запроса не соответствуют ожидаемым данным'})
    exit()

response = requests.delete("http://127.0.0.1:8000/vacancies/228", json=vacancy, verify=False)
data = str(response.json())
original_data = "{'error': 'vacancy not found'}"
if original_data != data:
    app_process.terminate()
    print({"verdict": 'WrongAnswer', 'error': '[DELETE] Данные с запроса не соответствуют ожидаемым данным'})
    exit()

print({"verdict": 'Ok'})
app_process.terminate()
