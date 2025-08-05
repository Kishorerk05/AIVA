🤖 AIVA Insurance Chatbot
A beautiful, modern insurance assistant chatbot with a glass-morphism UI design.

✨ Features
Beautiful Glass UI: Modern glass-morphism design with smooth animations

Insurance Expert: Powered by AI to provide insurance advice and information

Real-time Chat: Instant responses with typing indicators

Responsive Design: Works on desktop and mobile devices

Theme Toggle: Switch between dark and light themes

User Authentication: Simple username-based login system

🚀 Quick Start
Option 1: Using the Startup Script (Recommended)
Navigate to the project directory:

bash
cd aiva_chatbot
Run the startup script:

bash
python start_app.py
Open your browser and go to:

text
http://localhost:5000
Option 2: Manual Setup
Install dependencies:

bash
pip install -r requirements.txt
Start the server:

bash
python run.py
Open your browser and go to:

text
http://localhost:5000
🎯 How to Use
Login: Enter any username to start chatting

Chat: Type your insurance-related questions

Get Advice: AIVA will provide expert insurance guidance

Theme: Click the AI avatar to access theme settings

Logout: Use the logout option in the profile menu

🏗️ Project Structure
text
aiva_chatbot/
├── app/
│   ├── __init__.py
│   ├── chatbot.py      # AI chatbot logic
│   ├── config.py       # Configuration and LLM setup
│   └── routes.py       # Flask routes and API endpoints
├── UI/
│   └── index.html      # Beautiful chat interface
├── run.py              # Flask server entry point
├── start_app.py        # Automated startup script
├── requirements.txt    # Python dependencies
└── README.md           # This file
🔧 Configuration
The chatbot uses Groq LLM for responses. You need to set up your API key before using the chatbot.

Quick Setup
Get a Groq API Key: Sign up at https://console.groq.com/

Create a .env file in the project root with:

text
GROQ_API_KEY=gsk_your_actual_api_key_here
Test the connection: Visit http://localhost:5000/test after starting the server

For detailed setup instructions, see SETUP.md.

🎨 UI Features
Glass Morphism: Modern translucent design

Floating Elements: Animated background particles

Cursor Trail: Interactive mouse trail effect

Smooth Animations: Message slide-in effects

Responsive Layout: Adapts to different screen sizes

🛠️ Development
To modify the chatbot:

Backend Logic: Edit app/chatbot.py

API Routes: Modify app/routes.py

UI Design: Update UI/index.html

Styling: Modify CSS in the HTML file

📱 Browser Compatibility
Chrome (recommended)

Firefox

Safari

Edge

🚨 Troubleshooting
Port 5000 in use: Change the port in run.py

API errors: Check your Groq API key configuration

UI not loading: Ensure all files are in the correct directories

📄 License
This project is for educational and demonstration purposes.

Enjoy chatting with AIVA! 🤖💬

🗃️ Libraries Used
Web Frameworks
flask: Web framework for Python

flask-cors: Adds Cross-Origin Resource Sharing (CORS) support to Flask applications

fastapi: Modern and fast web framework for building APIs

uvicorn[standard]: ASGI server for running FastAPI applications

AI/ML Libraries
langchain: Framework for developing applications with language models

langchain-groq: Groq integration for LangChain

Utility Libraries
python-dotenv: Load environment variables from .env files

markdown: Python implementation of Markdown for rendering markdown text

email-validator: Email validation library

sendgrid: Email delivery service integration
