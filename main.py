from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import insert_update, all_submitted, get_all_updates
from openai_utils import generate_newsletter
from email_utils import send_newsletter
import shutil

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

HARDCODED_EMAILS = ["a@example.com", "b@example.com", "c@example.com"]

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})

@app.post("/submit")
async def submit(email: str = Form(...), text: str = Form(...), image: UploadFile = None):
    if email not in HARDCODED_EMAILS:
        return {"error": "Not allowed"}

    image_path = None
    if image:
        image_path = f"static/{email}_{image.filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    insert_update(email, text, image_path)

    if all_submitted(HARDCODED_EMAILS):
        updates = get_all_updates()
        newsletter = generate_newsletter(updates)
        send_newsletter(HARDCODED_EMAILS, newsletter)

    return {"message": "Submitted!"}
