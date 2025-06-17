from sqlalchemy import create_engine, Column, String, Text, Table, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///updates.db")
metadata = MetaData()
updates_table = Table(
    "updates", metadata,
    Column("email", String, primary_key=True),
    Column("text", Text),
    Column("image_path", String),
    Column("submitted_at", String),
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insert_update(email, text, image_path):
    session = Session()
    session.merge({"email": email, "text": text, "image_path": image_path, "submitted_at": str(datetime.utcnow())})
    session.commit()

def get_all_updates():
    session = Session()
    return session.query(updates_table).all()

def all_submitted(emails):
    session = Session()
    rows = session.query(updates_table).all()
    submitted = [row.email for row in rows]
    return all(email in submitted for email in emails)
