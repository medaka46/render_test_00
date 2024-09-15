import logging
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User
import pandas as pd

from datetime import datetime, timedelta, timezone

from starlette.middleware.sessions import SessionMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
async def login_signup(request: Request):
    message = "Please Log in or Sing up"
    message_color = "#0f0"
    
    start_date_adjust = 0
    
    # start_date = datetime.today() - timedelta(days = datetime.today().weekday()) # set up monday is start_date
    start_date = datetime.today() - timedelta(days = datetime.today().weekday() + start_date_adjust ) # set up monday is start_date
    date_sequence = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7*10)]  # 7*10 days sequence
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    request.session['start_date_adjust'] = start_date_adjust
    test_date = request.session.get('start_date_adjust')
    print(test_date)
    
    request.session['link_tab_page_active'] = "link_001"
    
    request.session['project_chart_switch'] = 1
    
    request.session['project_button_serect'] = "ID"
    
    request.session['project_id_order'] = 1
    
    
    
    
    # Your logic here, for example, returning a signup or login page
    # return templates.TemplateResponse("test01.html", {"request": request, "message": message, "message_color": message_color})
    # print("login_signup.html")
    return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
        

@app.post("/login_signup/add_user/")

async def add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
    try:
        db_user_check = db.query(User).filter(User.email == email).first()
        df_user = pd.read_csv('user.csv')
        
        logger.info(df_user)
        
        if db_user_check:
            message = "Sign up failed. Mail address were already used."
            message_color = "#f00"
            return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        else:
            df_user_check = df_user[(df_user['username'] == username) & (df_user['email'] == email)]
            if not df_user_check.empty:
                message = "Sign up was accepted. Please proceed to Log in."
                message_color = "#0f0"
                
                db_item = User(username=username, email=email, password=password)
                try:
                    db.add(db_item)
                    db.commit()
                    db.refresh(db_item)
                except Exception as e:
                    db.rollback()
                    message = f"An error occurred: {str(e)}"
                    message_color = "#f00"
                    logger.error(f"Database error: {str(e)}")
                
                return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
            
            else:
                message = "Sorry but you are not authorized to sign up."
                message_color = "#f00"
                
                return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return HTMLResponse(content=f"An unexpected error occurred: {str(e)}", status_code=500)
    
# --------------------

# async def add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
#     db_user_check = db.query(User).filter(User.email == email).first()
#     df_user = pd.read_csv('user.csv')
    
#     logger.info(df_user)
    
#     if db_user_check:
#         message = "Sign up failed. Mail address were already used."
#         message_color = "#f00"
#         return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
#     else:
#         df_user_check = df_user[(df_user['username'] == username) & (df_user['email'] == email)]
#         if not df_user_check.empty:
#             message = "Sign up was accepted. Please proceed to Log in."
#             message_color = "#0f0"
            
#             db_item = User(username=username, email=email, password=password)
#             try:
#                 db.add(db_item)
#                 db.commit()
#                 db.refresh(db_item)
#             except Exception as e:
#                 db.rollback()
#                 message = f"An error occurred: {str(e)}"
#                 message_color = "#f00"
#                 logger.error(f"Database error: {str(e)}")
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
#         else:
#             message = "Sorry but you are not authorized to sign up."
#             message_color = "#f00"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})


# # --------------------


# from fastapi import FastAPI, Depends, Request, Form
# from fastapi.responses import HTMLResponse

# from fastapi.templating import Jinja2Templates

# from datetime import datetime, timedelta, timezone

# from starlette.middleware.sessions import SessionMiddleware

# from passlib.context import CryptContext

# from .database import SessionLocal, engine, Base, Session

# from .models import User, Link, Schedule, Project

# import pandas as pd





# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




# app = FastAPI()

# # Set up Jinja2 templates
# templates = Jinja2Templates(directory="templates")

# app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # def hash_password(password):
# #     return pwd_context.hash(password)


# @app.get("/")
# async def login_signup(request: Request):
#     message = "Please Log in or Sing up"
#     message_color = "#0f0"
    
#     start_date_adjust = 0
    
#     # start_date = datetime.today() - timedelta(days = datetime.today().weekday()) # set up monday is start_date
#     start_date = datetime.today() - timedelta(days = datetime.today().weekday() + start_date_adjust ) # set up monday is start_date
#     date_sequence = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7*10)]  # 7*10 days sequence
#     today_date = datetime.today().strftime('%Y-%m-%d')
    
#     request.session['start_date_adjust'] = start_date_adjust
#     test_date = request.session.get('start_date_adjust')
#     print(test_date)
    
#     request.session['link_tab_page_active'] = "link_001"
    
#     request.session['project_chart_switch'] = 1
    
#     request.session['project_button_serect'] = "ID"
    
#     request.session['project_id_order'] = 1
    
    
    
    
#     # Your logic here, for example, returning a signup or login page
#     # return templates.TemplateResponse("test01.html", {"request": request, "message": message, "message_color": message_color})
#     # print("login_signup.html")
#     return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})


# @app.post("/login_signup/add_user/")

# async def add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
#     # hashed_password = hash_password(password)
    
#     db_user_check = db.query(User).filter(User.email == email).first()
#     df_user = pd.read_csv('user.csv')
    
#     print(df_user)
    
#     if db_user_check:
#         message = "Sign up failed. Mail address were already used."
#         message_color = "#f00"
#         return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
#     else:
#         df_user_check = df_user[(df_user['username'] == username) & (df_user['email'] == email)]
#         if not df_user_check.empty:
#             message = "Sign up was accepted. Please proceed to Log in."
#             message_color = "#0f0"
            
#             db_item = User(username=username, email=email, password=password)
#             try:
#                 db.add(db_item)
#                 db.commit()
#                 db.refresh(db_item)
#             except Exception as e:
#                 db.rollback()
#                 message = f"An error occurred: {str(e)}"
#                 message_color = "#0f0"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
#         else:
#             message = "Sorry but you are not authorized to sign up."
#             message_color = "#0f0"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
        
# --------------------

# async def add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
#     # hashed_password = hash_password(password)
    
#     db_user_check = db.query(User).filter(User.email == email).first()
#     df_user = pd.read_csv('user.csv')
    
#     print(df_user)
    
#     if db_user_check:
#         message = "Sign up failed. Mail address were already used."
#         message_color = "#f00"
#         return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
#     else:
#         df_user_check = df_user[(df_user['username'] == username) & (df_user['email'] == email)]
#         if not df_user_check.empty:
#             message = "Sign up was accepted. Please proceed to Log in."
#             message_color = "#0f0"
            
#             db_item = User(username=username, email=email, password=password)
#             try:
#                 db.add(db_item)
#                 db.commit()
#                 db.refresh(db_item)
#             except Exception as e:
#                 db.rollback()
#                 message = f"An error occurred: {str(e)}"
#                 message_color = "#0f0"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
#         else:
#             message = "Sorry but you are not authorized to sign up."
#             message_color = "#f00"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})

# async def add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
#     # hashed_password = hash_password(password)
    
#     db_user_check = db.query(User).filter(User.email == email).first()
#     df_user = pd.read_csv('user.csv')
    
#     print(df_user)
    
#     if db_user_check:
#         message = "Sign up failed. Mail address were already used."
#         message_color = "#f00"
#     # Your logic here, for example, returning a signup or login page
#         return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
#     else:
#         df_user_check = df_user[(df_user['username'] == username) & (df_user['email'] == email)]
#         # if df_user_check:
#         if not df_user_check.empty:
#     # Your logic here
#             message = "Sign up was accepted. Please procede Log in."
#             message_color = "#0f0"
            
#             db_item = User(username=username, email=email, password=password)
#             # db_item = User(username=username, email=email, password=hashed_password)
#             db.add(db_item)
#             db.commit()
#             db.refresh(db_item)
#         # Your logic here, for example, returning a signup or login page
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
        
#         else:
#             message = "Sorry but you are not authorized to sign up."
#             message_color = "#f00"
            
#             return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})