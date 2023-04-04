#! /bin/sh

source venv/bin/activate &&
pytest sdq && 
pip install ./sdq &&
gunicorn -w 1 'sdq.src.wsgi:app'
