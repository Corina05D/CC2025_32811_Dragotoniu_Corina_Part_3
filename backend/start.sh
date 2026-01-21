#!/bin/bash

#install dependencies
pip install -r requirements.txt

# start application FastAPI with gunicorn + uvicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT