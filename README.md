# 🤖 Reena Insurance Chatbot

A beautiful, modern insurance assistant chatbot with a glass-morphism UI design.

## ✨ Features

- **Beautiful Glass UI**: Modern glass-morphism design with smooth animations
- **Insurance Expert**: Powered by AI to provide insurance advice and information
- **Real-time Chat**: Instant responses with typing indicators
- **Responsive Design**: Works on desktop and mobile devices
- **Theme Toggle**: Switch between dark and light themes
- **User Authentication**: Simple username-based login system

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)

1. **Navigate to the project directory:**
   ```bash
   cd reena_chatbot
   ```

2. **Run the startup script:**
   ```bash
   python start_app.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python run.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## 🎯 How to Use

1. **Login**: Enter any username to start chatting
2. **Chat**: Type your insurance-related questions
3. **Get Advice**: Reena will provide expert insurance guidance
4. **Theme**: Click the AI avatar to access theme settings
5. **Logout**: Use the logout option in the profile menu

## 🏗️ Project Structure

```
reena_chatbot/
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
└── README.md          # This file
```

## 🔧 Configuration

The chatbot uses Groq LLM for responses. You need to set up your API key before using the chatbot.

### Quick Setup

1. **Get a Groq API Key**: Sign up at [https://console.groq.com/](https://console.groq.com/)
2. **Create a `.env` file** in the project root with:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```
3. **Test the connection**: Visit `http://localhost:5000/test` after starting the server

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 🎨 UI Features

- **Glass Morphism**: Modern translucent design
- **Floating Elements**: Animated background particles
- **Cursor Trail**: Interactive mouse trail effect
- **Smooth Animations**: Message slide-in effects
- **Responsive Layout**: Adapts to different screen sizes

## 🛠️ Development

To modify the chatbot:

1. **Backend Logic**: Edit `app/chatbot.py`
2. **API Routes**: Modify `app/routes.py`
3. **UI Design**: Update `UI/index.html`
4. **Styling**: Modify CSS in the HTML file

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🚨 Troubleshooting

- **Port 5000 in use**: Change the port in `run.py`
- **API errors**: Check your Groq API key configuration
- **UI not loading**: Ensure all files are in the correct directories

## 📄 License

This project is for educational and demonstration purposes.

---

**Enjoy chatting with Reena! 🤖💬**
