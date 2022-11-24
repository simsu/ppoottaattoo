import requests
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.crud.post import get_post, create_post
from database import SessionLocal
from routes import login

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")


class Picture():
    title: str = ""
    url: str = "https://flexible.img.hani.co.kr/flexible/normal/970/647/imgdb/original/2020/0312/20200312501932.jpg"


app.include_router(login.router)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    item = get_post(db)
    print(item)
    picture = Picture()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "banner": "https://img-cf.kurly.com/shop/data/goodsview/20210628/gv30000197759_1.jpg",
            "posts": item,
            "pictures": [picture for i in range(4)]
        })


@app.get("/edit", response_class=HTMLResponse)
async def show_edit_page(request: Request):
    return templates.TemplateResponse(
        "edit.html",
        {'request': request, }
    )


@app.post("/edit")
async def get_edit_page(request: Request, title: str = Form(), content: str = Form(), db: Session = Depends(get_db)):
    set_post = create_post(db, title, content)
    return set_post
