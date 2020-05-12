# microservices
 
### Local Setup


### 1 Run with docker
    $ docker-compose build
    $ docker-compose up

### 2 Initial migration
    $ docker-compose exec tasks python manage.py recreate_db


### 3 Populate data in databases
    $ docker-compose exec tasks python manage.py populate_db


### Run Tests
    $ docker-compose exec tasks python manage.py test


### Run flake8
    $ docker-compose run --rm tasks flake8
   

### Services
Service name| Service endpoint|
-------|---|
swagger|http://localhost:8084/
tasks|http://localhost:8081/v1/tasks/
react UI|http://localhost:3000/

virtual env for Windows 
$ virtualenv env 
$ .\venv2\Scripts\activate 
$ pip install -r requirements.txt