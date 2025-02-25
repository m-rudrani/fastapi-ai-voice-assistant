from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime
import google.auth
from google.cloud import dialogflow
import os
import uuid
import logging
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

# logging config
logging.basicConfig(filename="app.log",level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# db setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interactions.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# create interaction table
class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String, index=True)
    detected_intent = Column(String)
    ai_response = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# request model
class TextInput(BaseModel):
    text: str

# db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dialogflow setup
PROJECT_ID = os.getenv("PROJECT_ID")
SESSION_ID = os.getenv("SESSION_ID") 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def detect_intent(text: str):
    logging.info(f"Detecting intent for text: {text}")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    logging.info(f"Detected intent: {response.query_result.intent.display_name}, Response: {response.query_result.fulfillment_text}")
    return response.query_result.intent.display_name, response.query_result.fulfillment_text

# speech generation
def generate_speech(text):
    logging.info(f"Generating speech for text: {text}")
    tts = gTTS(text=text, lang="en")

    filename = f"static/{uuid.uuid4()}.mp3"
    tts.save(filename)
    logging.info(f"Speech saved to: {filename}")
    return filename

#input 
@app.post("/process")
def process_text(input: TextInput, db: Session = Depends(get_db)):
    try:
        logging.info(f"Received user input: {input.text}")
        detected_intent, ai_response = detect_intent(input.text)
        
        audio_file = generate_speech(ai_response)
        
        new_interaction = Interaction(user_input=input.text, detected_intent=detected_intent, ai_response=ai_response)
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        logging.info(f"Saved interaction to DB: {new_interaction.id}")

        return {
            "user_input": input.text,
            "intent": detected_intent,
            "response": ai_response,
            "audio_url": f"/{audio_file}" 
        }
    except Exception as e:
        logging.error(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# audio file 
@app.get("/static/{filename}")
def get_audio(filename: str):
    return FileResponse(f"static/{filename}", media_type="audio/mpeg")

# home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
