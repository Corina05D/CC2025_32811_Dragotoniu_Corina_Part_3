#!/bin/bash
# Activează virtualenv-ul creat de Oryx
source /home/site/wwwroot/antenv/bin/activate

# Asigură-te că ai ultima versiune de pip
pip install --upgrade pip

# Instalează toate dependențele
pip install -r requirements.txt

# pornește aplicația Streamlit
streamlit run app.py --server.port $PORT --server.address 0.0.0.0