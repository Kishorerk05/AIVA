# 🔧 Setup Guide for Reena Insurance Chatbot

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Groq API Key** - Get one from [Groq Console](https://console.groq.com/)

## Step 1: Get Your Groq API Key

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (it starts with `gsk_`)

## Step 2: Set Up Environment Variables

### Option A: Using .env file (Recommended)

1. Create a file named `.env` in the project root directory
2. Add your API key to the file:

```bash
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Option B: Using System Environment Variables

#### Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="gsk_your_actual_api_key_here"
```

#### Windows (Command Prompt):
```cmd
set GROQ_API_KEY=gsk_your_actual_api_key_here
```

#### macOS/Linux:
```bash
export GROQ_API_KEY="gsk_your_actual_api_key_here"
```

## Step 3: Test Your Setup

1. Start the server:
   ```bash
   python run.py
   ```

2. Test the connection:
   - Open your browser and go to: `http://localhost:5000/test`
   - You should see: `{"status": "success", "message": "🟢 Reena chatbot backend is running!", "api_ready": true}`

3. If `api_ready` is `false`, check your API key configuration

## Step 4: Start Chatting

1. Open your browser and go to: `http://localhost:5000`
2. Enter any username to start
3. Start chatting with Reena about insurance!

## Troubleshooting

### ❌ "GROQ_API_KEY not configured" Error
- Make sure you've set the environment variable correctly
- Restart your terminal/command prompt after setting the variable
- Check that the `.env` file is in the correct location

### ❌ "Internal server error" Error
- Check your internet connection
- Verify your Groq API key is valid
- Check the server console for detailed error messages

### ❌ Frontend not loading
- Make sure the server is running on port 5000
- Check that all files are in the correct directories
- Try clearing your browser cache

## Security Notes

- Never commit your `.env` file to version control
- Keep your API key secure and don't share it
- The `.env` file is already in `.gitignore` to prevent accidental commits

## Need Help?

If you're still having issues:
1. Check the server console for error messages
2. Verify your API key is working by testing it in the Groq console
3. Make sure all dependencies are installed: `pip install -r requirements.txt` 