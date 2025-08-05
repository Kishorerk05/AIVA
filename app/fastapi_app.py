from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import markdown
from app.chatbot import get_response
from app.config import GROQ_API_KEY

app = FastAPI()

# Enable CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to UI directory
UI_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'UI')

# Serve static files (for /static/*)
app.mount("/static", StaticFiles(directory=UI_PATH), name="static")

def render_markdown(text: str) -> str:
    """Convert markdown text to HTML with custom styling"""
    # Configure markdown with extensions for better rendering
    md = markdown.Markdown(extensions=['nl2br', 'tables', 'fenced_code'])
    
    # Convert markdown to HTML
    html_content = md.convert(text)
    
    # Add custom CSS styling for better presentation
    styled_html = f"""
    <div class="markdown-content" style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
    ">
        <style>
            .markdown-content h3 {{
                color: #2563eb;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 8px;
                margin-top: 20px;
                margin-bottom: 15px;
            }}
            .markdown-content ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            .markdown-content li {{
                margin: 5px 0;
                padding: 5px 0;
            }}
            .markdown-content strong {{
                color: #1f2937;
                font-weight: 600;
            }}
            .markdown-content table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                background: #f9fafb;
                border-radius: 8px;
                overflow: hidden;
            }}
            .markdown-content th, .markdown-content td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
            }}
            .markdown-content th {{
                background: #2563eb;
                color: white;
                font-weight: 600;
            }}
            .markdown-content tr:nth-child(even) {{
                background: #f3f4f6;
            }}
        </style>
        {html_content}
    </div>
    """
    
    return styled_html

@app.get("/", response_class=HTMLResponse)
def home():
    """Serve the UI/index.html file"""
    index_path = os.path.join(UI_PATH, 'index.html')
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path, media_type="text/html")

@app.get("/test")
def test():
    """Test endpoint to check if backend is working"""
    return {
        "status": "success",
        "message": "🟢 AIVA chatbot backend is running!",
        "api_ready": GROQ_API_KEY is not None
    }

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return JSONResponse({"error": "No message provided"}, status_code=400)
    if not GROQ_API_KEY:
        return JSONResponse({"error": "GROQ_API_KEY not configured. Please set your Groq API key in environment variables."}, status_code=500)
    try:
        response = get_response(user_input)
        
        # Return only the raw text - let the frontend handle markdown rendering
        return {"response": response}
    except Exception as e:
        return JSONResponse({"error": f"Internal server error: {str(e)}"}, status_code=500)

@app.post("/render-markdown")
async def render_markdown_endpoint(request: Request):
    """Convert markdown text to HTML"""
    data = await request.json()
    markdown_text = data.get("text", "")
    if not markdown_text:
        return JSONResponse({"error": "No text provided"}, status_code=400)
    
    try:
        html_content = render_markdown(markdown_text)
        return {"html": html_content}
    except Exception as e:
        return JSONResponse({"error": f"Markdown rendering error: {str(e)}"}, status_code=500)

@app.get("/{filename}")
def serve_static(filename: str):
    file_path = os.path.join(UI_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # Guess content type by extension (optional: could use mimetypes)
    return FileResponse(file_path)