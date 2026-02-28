# Social Media Manager Dashboard

A beautiful, modern dashboard for generating social media posts using Mistral AI.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Get your Mistral API Key:**
   - Sign up at [Mistral AI](https://console.mistral.ai/)
   - Generate an API key from your dashboard

3. **Start the server:**
   ```bash
   python run_server.py
   ```

4. **Open the dashboard:**
   Navigate to `http://localhost:8000` in your browser

## Features

- 🎨 **Modern UI** - Clean, responsive design with dark theme
- ⚡ **Fast Generation** - Powered by Mistral AI models
- 🔒 **Secure** - API key stored locally in browser
- 📋 **Easy Copy** - One-click copy to clipboard
- 🎯 **Model Selection** - Choose between Small, Medium, or Large models
- 💾 **Auto-save** - Your API key is remembered across sessions

## Usage

1. Enter your Mistral API key (stored securely in your browser)
2. Describe the social media post you want to create
3. Select the AI model (Small is fastest, Large is highest quality)
4. Click "Generate Post" and wait for the magic ✨
5. Copy the result and use it on your social media platforms!

## API Endpoints

- `GET /` - Dashboard UI
- `GET /health` - Health check
- `POST /generate-post` - Generate social media post

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter` - Submit form and generate post

## Development

The dashboard consists of:
- **Backend**: FastAPI server ([src/social_media_backend.py](src/social_media_backend.py))
- **Frontend**: HTML/CSS/JavaScript ([src/static/](src/static/))
- **Launcher**: Quick start script ([run_server.py](run_server.py))

## Troubleshooting

**Port already in use?**
Edit [run_server.py](run_server.py) and change the port number.

**API key not working?**
Make sure you're using a valid Mistral API key from https://console.mistral.ai/

**Can't connect to server?**
Check that the server is running and visit `http://localhost:8000`
