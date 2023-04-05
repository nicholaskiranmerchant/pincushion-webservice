#! /bin/sh

source venv/bin/activate &&
pytest sdq && 
flask --app sdq/src/wsgi:app --debug run
