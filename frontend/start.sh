#!/bin/bash

echo "Installing frontend requirements..."
pip install -r requirements.txt

# fallback port dacă $PORT nu e setat
export PORT=${PORT:-8501}

echo "Starting Streamlit app..."
# folosim exec ca Azure să monitorizeze procesul
exec streamlit run app.py --server.port $PORT --server.address 0.0.0.0