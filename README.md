# Bicoastal Bytes Foundations of Software Engineering Project
## Wheel of Jeopardy

### How to build
1. Install Poetry [Python Poetry Package Manager](https://python-poetry.org/docs/master/)
2. Change into `wheel-of-jeopardy` directory.
3. Run `poetry install` to install dependecies required for project.
4. Install docker.
5. Run `docker run -p 6379:6379 -d redis:5` to install the redis server needed for websockets.
6. Run `poetry shell` to get into the virtual environment.
7. Run `python manage.py migrate` to create database tables.
8. Run `python manage.py import_db` to import json data into the database. ONLY RUN ONCE!
9. Run `python manage.py runserver` to run the server.
10. Navigate to [localhost:8000](http://localhost:8000) to view the running server