#!/bin/bash

#pip install -r requirements.txt

#!/bin/bash
export PORT=${PORT:-8000}
exec gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
 