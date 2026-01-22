#!/bin/bash
set -e  # oprește scriptul dacă apare o eroare

# Directorul aplicației
APP_DIR="/home/site/wwwroot"
cd $APP_DIR

# Numele mediului virtual
VENV_NAME="antenv"

# Creează mediul virtual dacă nu există
if [ ! -d "$APP_DIR/$VENV_NAME" ]; then
    python3 -m venv $VENV_NAME
fi

# Activează mediul virtual
source "$APP_DIR/$VENV_NAME/bin/activate"

# Instalează / reinstalează dependențele
pip install --upgrade pip
pip install -r requirements.txt

# start Streamlit 
streamlit run app.py --server.port $PORT --server.address 0.0.0.0