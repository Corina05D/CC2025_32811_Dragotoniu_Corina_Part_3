#!/bin/bash
# Creează și activează mediul virtual dacă nu există
if [ ! -d "./antenv" ]; then
    python3 -m venv antenv
fi

# Activează mediul virtual
source ./antenv/bin/activate

# Instalează dependențele
pip install --upgrade pip
pip install -r requirements.txt

# pornește aplicația Streamlit
streamlit run app.py --server.port $PORT --server.address 0.0.0.0