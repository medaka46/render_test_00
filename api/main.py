from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_signup(request: Request):
    return templates.TemplateResponse("login_signup.html", {"request": request})

@app.get("/another", response_class=HTMLResponse)
async def another_page(request: Request):
    return templates.TemplateResponse("another_page.html", {"request": request})