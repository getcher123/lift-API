#!/bin/bash
python.exe -m pip install --upgrade pip
pip install --upgrade pydantic
pip install -r requirements.txt
python -m spacy download ru_core_news_sm