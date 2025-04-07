# app/__init__.py
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
