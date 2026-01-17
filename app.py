import gradio as gr
import subprocess
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
api_app = FastAPI(title="yt-dlp Command Executor API")

# Pydantic model for request validation
class YtDlpRequest(BaseModel):
    url: str
    args: str = ""  # Additional yt-dlp arguments

def execute_ytdlp(url, args=""):
    """
    Execute yt-dlp command directly
    Returns: (success, message, output, file_paths)
    """
    try:
        # Create output directory
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        # Build yt-dlp command
        cmd = ["yt-dlp", url]

        # Add output directory
        cmd.extend(["-o", f"{output_dir}/%(title)s.%(ext)s"])

        # Add additional arguments if provided
        if args:
            # Split arguments properly (handle quoted strings)
            import shlex
            arg_list = shlex.split(args)
            cmd.extend(arg_list)

        # Execute the command
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        output = result.stdout
        error = result.stderr

        if result.returncode == 0:
            # Try to find downloaded files
            downloaded_files = []
            if os.path.exists(output_dir):
                # Get recently modified files
                files = [
                    f for f in os.listdir(output_dir)
                    if os.path.isfile(os.path.join(output_dir, f))
                ]
                downloaded_files = files

            return True, "✅ Command executed successfully!", output, downloaded_files
        else:
            return False, f"❌ Error: {error}", error, []

    except subprocess.TimeoutExpired:
        return False, "❌ Error: Command timed out after 5 minutes", "", []
    except Exception as e:
        return False, f"❌ Error: {str(e)}", "", []

def gradio_execute_ytdlp(url, args):
    """Gradio interface function"""
    if not url:
        return "❌ Please provide a URL"

    success, message, output, files = execute_ytdlp(url, args)

    result_text = f"{message}\n\n"
    result_text += f"Command output:\n{output}\n\n"

    if files:
        result_text += f"Downloaded files:\n" + "\n".join(files)
        result_text += f"\n\nFiles are in: {os.path.abspath('downloads')}"

    return result_text

@api_app.post("/execute")
async def api_execute_ytdlp(request: YtDlpRequest):
    """
    API endpoint to execute yt-dlp command
    Parameters:
    - url: Video URL (required)
    - args: Additional yt-dlp arguments (optional)

    Example for video segment:
    args = "--download-sections *00:00:10-00:01:30"

    Example for audio only:
    args = "--extract-audio --audio-format mp3"

    Example for best quality:
    args = "-f best"
    """
    try:
        success, message, output, files = execute_ytdlp(request.url, request.args)

        return {
            "success": success,
            "message": message,
            "output": output,
            "downloaded_files": files,
            "download_dir": "downloads"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_app.get("/api/files/{filename}")
async def get_file(filename: str):
    """Serve downloaded files"""
    file_path = os.path.join("downloads", filename)
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            filename=filename
        )
    raise HTTPException(status_code=404, detail="File not found")

@api_app.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "yt-dlp Command Executor API",
        "endpoints": {
            "execute": "POST /api/execute - Execute yt-dlp command",
            "files": "GET /api/files/{filename} - Download the file"
        },
        "examples": {
            "video_segment": {
                "url": "https://youtube.com/watch?v=...",
                "args": "--download-sections *00:00:10-00:01:30"
            },
            "audio_only": {
                "url": "https://youtube.com/watch?v=...",
                "args": "--extract-audio --audio-format mp3"
            },
            "best_quality": {
                "url": "https://youtube.com/watch?v=...",
                "args": "-f bestvideo+bestaudio --merge-output-format mp4"
            },
            "subtitle_only": {
                "url": "https://youtube.com/watch?v=...",
                "args": "--write-subs --skip-download"
            }
        }
    }

# Create Gradio interface
def create_gradio_interface():
    with gr.Blocks(
        title="yt-dlp Command Executor",
        theme=gr.themes.Soft()
    ) as demo:
        gr.Markdown(
            """
            # 🎬 yt-dlp Command Executor

            Execute yt-dlp commands via a web interface or API!

            ## Quick Examples:

            ### Video Segment (00:00:10 to 00:01:30)
            ```
            --download-sections *00:00:10-00:01:30
            ```

            ### Audio Only (MP3)
            ```
            --extract-audio --audio-format mp3
            ```

            ### Best Quality Video
            ```
            -f bestvideo+bestaudio --merge-output-format mp4
            ```

            ### Download Subtitles Only
            ```
            --write-subs --skip-download
            ```

            ### List Formats
            ```
            --list-formats
            ```

            ### Playlist Download
            ```
            --yes-playlist
            ```

            ## API Usage:

            ```bash
            curl -X POST http://localhost:7860/api/execute \\
              -H "Content-Type: application/json" \\
              -d '{
                "url": "https://youtube.com/watch?v=...",
                "args": "--download-sections *00:00:10-00:01:30"
              }'
            ```

            ## More yt-dlp Options:
            Visit https://github.com/yt-dlp/yt-dlp for full documentation
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                url_input = gr.Textbox(
                    label="Video URL",
                    placeholder="https://youtube.com/watch?v=...",
                    value="",
                    lines=2
                )

            with gr.Column(scale=1):
                args_input = gr.Textbox(
                    label="Additional yt-dlp Arguments",
                    placeholder="--download-sections *00:00:10-00:01:30",
                    value="--download-sections *00:00:10-00:00:30",
                    lines=2
                )

        with gr.Row():
            execute_btn = gr.Button("🚀 Execute yt-dlp", variant="primary", size="lg")

        with gr.Row():
            output_text = gr.Textbox(
                label="Output",
                placeholder="Command output will appear here...",
                interactive=False,
                lines=15
            )

        # Example section
        gr.Markdown("### 📝 Quick Examples")
        gr.Examples(
            examples=[
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "--download-sections *00:00:10-00:00:30"],
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "--extract-audio --audio-format mp3"],
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "-f best"],
                ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "--list-formats"],
            ],
            inputs=[url_input, args_input],
            label="Try these examples"
        )

        # Button click event
        execute_btn.click(
            fn=gradio_execute_ytdlp,
            inputs=[url_input, args_input],
            outputs=output_text
        )

        gr.Markdown(
            """
            ---
            ### 🔗 API for n8n

            **Endpoint**: `POST /api/execute`

            **Body**:
            ```json
            {
              "url": "https://youtube.com/watch?v=...",
              "args": "--download-sections *00:00:10-00:01:30"
            }
            ```

            **Response**:
            ```json
            {
              "success": true,
              "message": "✅ Command executed successfully!",
              "output": "...",
              "downloaded_files": ["video.mp4"],
              "download_dir": "downloads"
            }
            ```

            **Download files**: `GET /api/files/{filename}`
            """
        )

    return demo

if __name__ == "__main__":
    # Mount FastAPI app to Gradio
    demo = create_gradio_interface()
    demo = gr.mount_gradio_app(api_app, demo, path="/")

    # Run both Gradio and FastAPI
    uvicorn.run(api_app, host="0.0.0.0", port=7860)
