from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from sql_app import models, crud, schemas
from sql_app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="./sql_app/templates")


@app.post("/user", response_model=schemas.User)
async def create_user(username: str = Form(), db: Session = Depends(get_db)):
    be_user = schemas.UserCreate(username=username)
    db_user = crud.create_user(db=db, user=be_user)
    return db_user


@app.get("/user/{username}", response_model=schemas.UserBase, response_class=HTMLResponse)
async def read_user(request: Request, username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": db_user})


@app.get("/user", response_class=HTMLResponse)
async def read_user(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})



@app.get("/item/{id}", response_class=HTMLResponse)
async def read_user(request: Request, id: int):
    return templates.TemplateResponse("user.html", {"request": request, "item_id": id})
