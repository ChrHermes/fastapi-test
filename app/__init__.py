# app/__init__.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Statische Dateien bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")
