# Simple TODO APP API

The API is implemented using Flask( version 1.1.1)

## Installing requirements
All requirements are in requirements.txt

Doing:
```
pip install -r requirements.txt
```
Will install all needed packages

## Running the app
The app is very basic Flask app, so it is very easy to run

For API description read: [API doc](api-doc.md)

### Windows
```
> cd project_dir
> set FLASK_APP=app.py
> venv\Scripts\flask.exe run
```

### Linux (Not tested)
```
> cd project_dir
> export FLASK_APP=app.py
> flask run
```

## Running the tests
There are functional py.test tests 
you can run them with

```
> cd project_dir
> pytest -v
```
