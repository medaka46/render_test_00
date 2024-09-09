from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from .database import SessionLocal, engine, Base, Session


app = FastAPI()


# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def login_signup(request: Request):
    message = "Please Log in or Sign up"
    message_color = "#f00"
    return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
# 
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("static/test_00.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content=html_content)




# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("templates/login_signup.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content=html_content)





# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# # Set up Jinja2 templates
# templates = Jinja2Templates(directory="templates")

# # Mount static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def login_signup(request: Request):
#     message = "Please Log in or Sign up"
#     message_color = "#0f0"
#     return templates.TemplateResponse("test_00.html", {"request": request, "message": message, "message_color": message_color})


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def health_check():
#     return "The health cjeck is successful!"