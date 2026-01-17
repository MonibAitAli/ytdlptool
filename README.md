# 🎬 Simple yt-dlp Command Executor

A simple web interface and API that executes yt-dlp commands. Just provide a URL and any yt-dlp arguments - full flexibility!

## ✨ Features

- 🌐 **Web Interface**: Simple Gradio UI
- 🔌 **REST API**: Easy HTTP API for automation
- ⚡ **Full yt-dlp Power**: Use any yt-dlp argument you want
- 🎬 **Video Segments**: Download specific parts of videos
- 🎵 **Audio Extraction**: Convert videos to MP3/M4A
- 📝 **Subtitles**: Download subtitles
- 📋 **Playlists**: Download whole playlists or parts

## 🚀 Quick Start

### On Railway (Recommended) ⭐

1. Go to [railway.app](https://railway.app) and sign up/login
2. Click **New Project** → **Deploy from GitHub**
3. Or **New Project** → **Empty Project** then upload files
4. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `railway.toml`
   - `Procfile`
5. Click **Deploy** - Railway will detect Python automatically
6. Your app will be live in 1-2 minutes!
7. Get your app URL from Railway dashboard

**Important**: Make sure you set up a Railway account and have your GitHub connected, or use the direct upload option.

### Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Install yt-dlp (if not already installed)
pip install yt-dlp

# Run the app
python app.py
```

Access at:
- **Web UI**: `http://localhost:7860`
- **API Docs**: `http://localhost:7860/docs`

## 📖 Usage

### Web Interface

1. **Paste Video URL**
2. **Add yt-dlp Arguments** (optional)
3. **Click "Execute yt-dlp"**

### API Usage

**Endpoint**: `POST /api/execute`

**Request**:
```json
{
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "args": "--download-sections *00:00:10-00:01:30"
}
```

**Response**:
```json
{
  "success": true,
  "message": "✅ Command executed successfully!",
  "output": "[yt-dlp output]",
  "downloaded_files": ["Video Title.mp4"],
  "download_dir": "downloads"
}
```

**Download Files**: `GET /api/files/{filename}`

## 🎯 Common Use Cases

### 1. Download Video Segment (00:00:10 to 00:01:30)
```
args: --download-sections *00:00:10-00:01:30
```

### 2. Extract Audio as MP3
```
args: --extract-audio --audio-format mp3
```

### 3. Best Quality Video
```
args: -f bestvideo+bestaudio --merge-output-format mp4
```

### 4. Download Subtitles Only
```
args: --write-subs --skip-download
```

### 5. List Available Formats
```
args: --list-formats
```

### 6. Download Playlist (First 5 Videos)
```
args: --yes-playlist --playlist-end 5
```

### 7. Max 720p Quality
```
args: -f "best[height<=720]"
```

### 8. Last 60 Seconds
```
args: --download-sections *-00:01:00
```

### 9. From 00:00:10 for 60 seconds
```
args: --download-sections *00:00:10-+00:01:00
```

### 10. Embed Subtitles & Thumbnail
```
args: --embed-subs --embed-thumbnail
```

## 🔌 n8n Integration

### HTTP Request Node Configuration

**Method**: POST
**URL**: `http://your-app-url/api/execute`
**Body** (JSON):

```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "args": "--download-sections *00:00:10-00:01:30"
}
```

### Complete Workflow Example

1. **Webhook Trigger** - Receives URL and args
2. **HTTP Request** - Calls `/api/execute`
3. **Process Results** - Handle downloaded files

### Test with curl

```bash
curl -X POST http://localhost:7860/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
    "args": "--extract-audio --audio-format mp3"
  }'
```

## 📁 File Structure

```
ytdlp-tool/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── railway.toml              # Railway configuration
├── Procfile                  # Railway process file
├── README.md                 # This file
├── YT-DLP-CHEATSHEET.md      # Common commands reference
├── test_api.py               # Test script
└── downloads/                # Downloaded files (auto-created)
```

## 📚 More Examples

Check out **`YT-DLP-CHEATSHEET.md`** for:
- Video download options
- Audio extraction formats
- Subtitle handling
- Playlist management
- Advanced features
- Format selection
- Authentication

## 🔧 Requirements

- Python 3.8+
- gradio
- yt-dlp
- fastapi
- uvicorn
- pydantic

See `requirements.txt` for exact versions.

## 🎓 yt-dlp Documentation

For full yt-dlp documentation:
- **GitHub**: https://github.com/yt-dlp/yt-dlp
- **Docs**: https://yt-dlp.readthedocs.io/

## 🐛 Troubleshooting

### yt-dlp not found
```bash
pip install yt-dlp
```

### Permission denied on download
Check that the `downloads` folder is writable.

### Command timeout
The app has a 5-minute timeout per command. Adjust in `app.py` if needed.

## 💡 Tips

1. **Use `--list-formats` first** to see available options
2. **Combine multiple args**: `--extract-audio --audio-format mp3 --audio-quality 0`
3. **Quote args with spaces**: `"-f bestvideo[ext=mp4]+bestaudio[ext=m4a]"`
4. **Test in terminal first**: `yt-dlp [url] [args]`

---

**Simple, flexible, powerful! 🚀**
"# ytdlptool" 
