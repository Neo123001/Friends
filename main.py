from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import uuid, os
from dotenv import load_dotenv

from models import Update
from store import add_update, get_all_updates, clear_updates
from openai_utils import generate_newsletter
from email_utils import send_newsletter_email

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit(email: str = Form(...), text: str = Form(""), file: UploadFile = File(None)):
    image_path = None
    if file and file.filename:
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        image_path = f"{upload_folder}/{uuid.uuid4().hex}_{file.filename}"
        with open(image_path, "wb") as f:
            f.write(await file.read())

    update = Update(email=email, text=text, image_path=image_path)
    add_update(update)
    return RedirectResponse("/", status_code=303)

@app.get("/send-newsletter")
def send_newsletter():
    updates = get_all_updates()
    if not updates:
        return {"message": "No updates yet."}

    newsletter = generate_newsletter(updates)
    recipients = list({u.email for u in updates if u.email})
    send_newsletter_email(
        subject="🗞️ Community Newsletter",
        content=newsletter,
        recipients=recipients
    )
    clear_updates()
    return {"message": f"Newsletter sent to {len(recipients)} users."}
