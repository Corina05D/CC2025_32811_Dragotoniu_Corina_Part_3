#!/bin/bash

#install dependencies
pip install -r requirements.txt

# start Streamlit 
streamlit run app.py --server.port $PORT --server.address 0.0.0.0