import logging
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User, Schedule
import pandas as pd

from datetime import datetime, timedelta, timezone

from starlette.middleware.sessions import SessionMiddleware

from fastapi.responses import RedirectResponse # from slalchemy import create_engine, Column, Integer, String

from zoneinfo import ZoneInfo

import json




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

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})
        
        

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

start_date = datetime.today() - timedelta(days = datetime.today().weekday()) # set up monday is start_date

date_sequence = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7*10)]  # 7*10 days sequence

today_date = datetime.today().strftime('%Y-%m-%d')




@app.post("/login_signup/check_user/")

async def check_user(request: Request, date_sequence = date_sequence, today_date = today_date, username: str = Form(...), email: str = Form(...), password: str = Form(None), db: Session = Depends(get_db)):
    # hashed_password = hash_password(password)
    # login_username = username
    # db_user = db.query(User).filter(User.username == username, User.email == email, User.password == hashed_password).first()
    db_user = db.query(User).filter(User.username == username, User.email == email, User.password == password).first()
    # db_user = db.query(User).filter(User.username == username and User.email == email and User.password == hashed_password).first()
    # db_user = db.query(User).filter(User.username == username and User.email == email and User.password == hashed_password).first()
    
    print(User.password)
    
    if db_user:
        
        
        login_username = username
        time_zone_message = "Please select Time zone :"
        message_color = "#f00"
        
        return templates.TemplateResponse("schedule_indicate_00.html", {"request": request, "dates": date_sequence, "today": today_date, "login_username": login_username, "time_zone_message": time_zone_message, "message_color": message_color})
        # return templates.TemplateResponse("login_ok.html", {"request": request, "dates": date_sequence, "today": today_date})
    else:
        message = "Log in failed. Please try again"
        message_color = "#f00"
    # Your logic here, for example, returning a signup or login page
        return templates.TemplateResponse("login_signup.html", {"request": request, "message": message, "message_color": message_color})
    
    
# --------------------

@app.post("/schedule/select_time_zone/")    
async def create_item(request: Request, login_username: str = Form(...), time_zone: str = Form(...), db: Session = Depends(get_db)):


    request.session['login_username'] = login_username  # Save to session
    request.session['time_zone'] = time_zone  # Save to session

    # Log the size of the response content
    response_content = json.dumps({"login_username": login_username, "time_zone": time_zone})
    response_size = len(response_content)
    logger.info(f"Response size: {response_size} bytes")

    return RedirectResponse("/schedule/", status_code=303)
    # global active_meeting
    # global local_time_zone
    # # global login_username
    
    # # local_time_zone = time_zone
    # # time_zone_2 = "Osaka"
    
    # print(time_zone)
    # print(login_username)
    # request.session['login_username'] = login_username  # Save to session
    # request.session['time_zone'] = time_zone  # Save to session
    # # url = str(request.url_for('get_tasks')) + f"?time_zone={time_zone}"
    
    # # url = request.url_for('get_tasks') + f"?time_zone={time_zone}"
    # # return RedirectResponse(url, status_code=303)
    
    
    # # singapore
    # return RedirectResponse("/schedule/", status_code=303)

# --------------------

@app.get("/schedule/")
async def schedule(request: Request, time_zone: str = "UTC", db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    login_username = request.session.get('login_username')
    time_zone = request.session.get('time_zone', time_zone)
    logger.info(f"Time zone is {time_zone}")

    tasks = db.query(Schedule).order_by(Schedule.start_datetime).offset(skip).limit(limit).all()

    start_date_adjust = request.session.get('start_date_adjust', 0)
    start_date = datetime.today() - timedelta(days=datetime.today().weekday() + start_date_adjust)
    date_sequence = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7*10)]
    today_date = datetime.today().strftime('%Y-%m-%d')

    data = [{
        'id': task.id,
        'name': task.name,
        'start_datetime': task.start_datetime,
        'end_datetime': task.end_datetime,
        'link': task.link,
        'category': task.category,
        'status': task.status,
        'id_user': task.id_user
    } for task in tasks]

    df_tasks = pd.DataFrame(data)
    df_tasks['start_datetime'] = pd.to_datetime(df_tasks['start_datetime']).dt.tz_localize('UTC')
    df_tasks['end_datetime'] = pd.to_datetime(df_tasks['end_datetime']).dt.tz_localize('UTC')

    local_start_dates = []
    local_start_times = []
    local_end_dates = []
    local_end_times = []

    for i in range(len(df_tasks)):
        df_task = df_tasks.iloc[i]
        local_start_datetime = df_task["start_datetime"].astimezone(ZoneInfo(time_zone))
        local_start_date = local_start_datetime.date()
        local_start_time = local_start_datetime.time().strftime("%H:%M")
        local_start_dates.append(str(local_start_date))
        local_start_times.append(str(local_start_time))

        local_end_datetime = df_task["end_datetime"].astimezone(ZoneInfo(time_zone))
        local_end_date = local_end_datetime.date()
        local_end_time = local_end_datetime.time().strftime("%H:%M")
        local_end_dates.append(str(local_end_date))
        local_end_times.append(str(local_end_time))

    df_local_start_dates = pd.DataFrame(local_start_dates, columns=['local_start_date'])
    df_local_start_times = pd.DataFrame(local_start_times, columns=['local_start_time'])
    df_local_end_dates = pd.DataFrame(local_end_dates, columns=['local_end_date'])
    df_local_end_times = pd.DataFrame(local_end_times, columns=['local_end_time'])
    
    df_combined = pd.concat([df_tasks, df_local_start_dates, df_local_start_times, df_local_end_dates, df_local_end_times], axis=1)
    
    
    # Convert Timestamp objects to strings
    df_combined = df_combined.applymap(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
    

    # df_combined = pd.concat([df_tasks, df_local_start_dates, df_local_start_times, df_local_end_dates, df_local_end_times], axis=1)
    df_combined_dict = df_combined.to_dict(orient='records')
    length_df_combined = len(df_combined)

    time_zone_message = "Current time zone :"
    message_color = "#0f0"
    tab_page_active = "schedule"

    # Log the size of the response content
    response_content = json.dumps(df_combined_dict)
    response_size = len(response_content)
    logger.info(f"Response size: {response_size} bytes")

    return templates.TemplateResponse("schedule_indicate_00.html", {
        "request": request,
        "df_combined": df_combined_dict,
        "dates": date_sequence,
        "today": today_date,
        "time_zone": time_zone,
        "length_df_combined": length_df_combined,
        "local_start_date": local_start_date,
        "local_start_time": local_start_time,
        "time_zone_message": time_zone_message,
        "message_color": message_color,
        "login_username": login_username,
        "tab_page_active": tab_page_active
    })

# @app.get("/schedule/")
# async def schedule(request: Request, time_zone: str = "UTC", db: Session = Depends(get_db), date_sequence = date_sequence, today_date = today_date):  
# # async def get_tasks(request: Request, db: Session = Depends(get_db), date_sequence = date_sequence, today_date = today_date):
# # async def get_tasks(request: Request, db: Session = Depends(get_db), date_sequence = date_sequence, today_date = today_date, login_username = login_username):
#     # global local_time_zone
#     # global active_meeting
#     login_username = request.session.get('login_username')
#     time_zone = request.session.get('time_zone')
#     # today_date = request.session.get('today_date')
#     print(f"time_zone is {time_zone}")
    
#     # tasks = db.query(Meeting).order_by(Meeting.name).all()
#     tasks = db.query(Schedule).order_by(Schedule.start_datetime).all()
    
#     start_date_adjust = request.session.get('start_date_adjust')
    
#     start_date = datetime.today() - timedelta(days = datetime.today().weekday() + start_date_adjust ) # set up monday is start_date
#     date_sequence = [str((start_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7*50)]  # 7*10 days sequence
#     today_date = datetime.today().strftime('%Y-%m-%d')
    
    
    
    
    
#     # users = db.query(User).order_by(User.start_datetime).all()
    
#     data = [{
#     'id': task.id,
#     'name': task.name,
#     'start_datetime': task.start_datetime,
#     'end_datetime': task.end_datetime,
#     'link': task.link,
#     'category': task.category,
#     'status': task.status,
#     'id_user': task.id_user
#     } for task in tasks]

#     # df_tasks = pd.DataFrame(data)
#     # print(tasks.start_datetime)
    
    
#     df_tasks = pd.DataFrame(data)
#     # print("df_tasks", df_tasks)
#     # print(df_tasks)
    
#     # print(df_tasks.iloc[0]['name'])
#     local_start_dates = []
#     local_start_times = []
#     local_end_dates = []
#     local_end_times = []
    
#     df_tasks['start_datetime'] = df_tasks['start_datetime'].dt.tz_localize('UTC')
#     df_tasks['end_datetime'] = df_tasks['end_datetime'].dt.tz_localize('UTC')
#     # df_tasks['start_datetime'] = df_tasks['start_datetime'].dt.tz_localize('UTC').dt.tz_convert(ZoneInfo(local_time_zone))
    
    
#     for i in range(len(df_tasks)):
#         df_task = df_tasks.iloc[i]
    
    
#         local_start_datetime = df_task["start_datetime"].astimezone(ZoneInfo(time_zone))
#         # local_start_datetime = df_task["start_datetime"].astimezone(ZoneInfo(local_time_zone))
#     # #     # local_start_datetime = df_task.start_datetime.astimezone(ZoneInfo(local_time_zone))
#         local_start_date = local_start_datetime.date()
#         local_start_time = local_start_datetime.time().strftime("%H:%M")
        
        
#     # #     print(f"Local Time in {local_time_zone}:", local_start_date)
#         local_start_dates.append(str(local_start_date))
#         local_start_times.append(str(local_start_time))
        
        
#         local_end_datetime = df_task["end_datetime"].astimezone(ZoneInfo(time_zone))
#         # local_end_datetime = df_task["end_datetime"].astimezone(ZoneInfo(local_time_zone))
#     # #     # local_end_datetime = df_task.end_datetime.astimezone(ZoneInfo(local_time_zone))
#         local_end_date = local_end_datetime.date()
#         local_end_time = local_end_datetime.time().strftime("%H:%M")
        
        
#     # #     print(f"Local Time in {local_time_zone}:", local_end_date)
#         local_end_dates.append(str(str(local_end_date)))
        
#         local_end_times.append(str(local_end_time))
        
#     df_local_start_dates = pd.DataFrame(local_start_dates, columns=['local_start_date'])
#     df_local_start_times = pd.DataFrame(local_start_times, columns=['local_start_time'])
    
#     df_local_end_dates = pd.DataFrame(local_end_dates, columns=['local_end_date'])
#     df_local_end_times = pd.DataFrame(local_end_times, columns=['local_end_time'])
   
    
#     df_combined = pd.concat([df_tasks, df_local_start_dates, df_local_start_times, df_local_end_dates, df_local_end_times], axis=1)
#     # request.session['df_combined'] = df_combined  # Save to session
#     # print("df_combined", df_combined)
#     print(df_combined)
    
#     df_combined_dict = df_combined.to_dict(orient='records')
    
#     length_df_combined = len(df_combined)
    
#     time_zone_massage = "Current time zone :"
    
#     message_color = "#0f0"
    
#     tab_page_active = "schedule"
    
#     # print("df_combined", df_combined)
    
    
    
    
#     return templates.TemplateResponse("schedule_indicate_00.html", {"request": request, "df_combined": df_combined_dict, "dates": date_sequence, "today": today_date, "time_zone": time_zone, "length_df_combined": length_df_combined, "local_start_date": local_start_date,"local_start_time": local_start_time, "time_zone_massage": time_zone_massage, "message_color": message_color, "login_username": login_username, "tab_page_active": tab_page_active})
