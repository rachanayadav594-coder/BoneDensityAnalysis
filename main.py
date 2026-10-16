from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
import os
from dotenv import load_dotenv
from routers import auth, bone_density
from utils.csv_handler import init_csvs
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_csvs()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(bone_density, prefix="/bd", tags=["bone_density"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    return response
