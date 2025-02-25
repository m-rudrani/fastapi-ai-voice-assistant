# FastAPI AI Assistant

## 📌 Overview
This project is a **voice-enabled AI assistant** built using **FastAPI**, **Dialogflow**, and **gTTS** (Google Text-to-Speech). It allows users to interact via text, receive AI-generated responses, and hear them through synthesized speech.

## 🚀 Features
- **FastAPI Backend**: A lightweight and high-performance web API.
- **Dialogflow Integration**: AI-powered intent detection and responses.
- **Text-to-Speech**: Converts AI responses into speech using `gTTS`.
- **SQLite Database**: Stores user interactions for future reference.
- **Logging**: Tracks API requests and errors in `app.log`.
- **Static File Hosting**: Serves generated audio files for playback.

## 📦 Installation
### ** 1️ Clone the Repository**
```sh
git clone https://github.com/your-repo/fastapi-ai-assistant.git
cd fastapi-ai-assistant
```

### ** 2️ Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### ** 3️ Install Dependencies**
```sh
pip install -r requirements.txt
```

### ** 4️ Set Up Environment Variables**
Create a `.env` file in the project root and add:
```
PROJECT_ID=your-dialogflow-project-id
SESSION_ID=12345
GOOGLE_APPLICATION_CREDENTIALS=path/to your-service-account.json
DATABASE_URL=sqlite:///./interactions.db
```

## Running the Application
Start the FastAPI server:
```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Access the UI at: **http://127.0.0.1:8000/**


## 🔧 Setting Up Dialogflow
### **Go to Dialogflow Console:**
[Dialogflow Console](https://dialogflow.cloud.google.com/)

### **Create an Agent**
1. Click **"Create Agent"**.
2. Select Your Google Cloud Project (**voice-452008** or the correct one).
3. **Set Agent Details:**
   - **Agent Name**: (e.g., `VoiceAssistant`)
   - **Default Language**: Choose your preferred language (e.g., English).
   - **Google Project**: Select 'project id' from Google Cloud Project(or the create project).
4. Click **"Create"** and wait for Dialogflow to set up the agent.
5. Go to **"Intents"** and create a simple test intent.

## 🐳 Docker Setup
### **Build the Docker Image**
```sh
docker build -t fastapi-ai-assistant .
```
### **Run the Container**
```sh
docker run -p 8000:8000 fastapi-ai-assistant
```

## 📜 License
This project is licensed under the **MIT License**.
