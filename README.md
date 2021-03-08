# big5-app

08/03: Despite content may change, this README might not get updated.

This is my attempt at setting up a development and production server/database using Python, Flask and Heroku. There is a number of things I find worth documenting. This was a undergrad thesis side-project, mostly to centralise operations.

## Folder directory structure

```
big5-app
├── config
├── migrations
├── server
│   ├── __init.py__
│   ├── ext.py
│   ├── main.py
│   └── models.py
├── .env (*)
├── .flaskenv
├── Pipfile
├── Procfile
├── requirements.txt
└── runtime.txt
```

* `config.py`: Config files for development and production. The development config file retrieves the database URI from .env, but the production config file retrieves the database URI from Heroku's set environment variable.
* `migrations`: Folder to store database's migrations
* `server`:
  * `__init.py__`: Flask application factory
  * `ext.py`: Initialises a common DB instance
  * `main.py`: Flask blueprint for endpoints
  * `models.py`: Database models
* `.env`: Details local database URI, needs `python-dotenv` library.
* `.flaskenv`: Details Flask enviornment variables: `FLASK_APP` and `FLASK_ENV`. Both are for development, as these are handeled in other places for production.
* `Pipfile`: `pipenv`'s virtual environment requirements folder.
* `Procfile`: command line for starting the application on heroku.
* `requirements.txt`: standard requirements.txt file, can be derived from `pipenv`: `pipenv run pip freeze > requirements.txt`.
* `runtime.txt`: states utilisied Python version, Heroku needs to know this.

## Useful commands

I won't explain why as I honestly won't bother. But I may need a reminder in the future...

```
pipenv install #
pipenv shell
pipenv run pip freeze > requirements.txt
flask run
flask db init
flask db migrate
flask db upgrade
flask db stamp head
heroku login
heroku create #
heroku git:remote -a #
heroku config:set FLASK_ENV=production
heroku config --app #
heroku logs --tail
heroku run flask db upgrade
git push heroku HEAD:master
```