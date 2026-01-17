# yt-dlp Quick Reference

Common yt-dlp commands to use with the app.

## 🎬 Video Download Examples

### Basic Download
```
(no args needed)
```
Downloads the video in best available quality.

### Best Quality (merge video+audio)
```
-f bestvideo+bestaudio --merge-output-format mp4
```
Downloads best video and audio separately, then merges into MP4.

### Specific Quality
```
-f "best[height<=720]"
```
Downloads video with max 720p resolution.

### Video Segment (Start to End)
```
--download-sections *00:00:10-00:01:30
```
Downloads from 00:00:10 to 00:01:30.

### Video Segment (Start to End + Duration)
```
--download-sections *00:00:10-+00:01:30
```
Downloads starting at 00:00:10 for 1 minute 30 seconds.

### Last X Seconds
```
--download-sections *-00:01:30
```
Downloads last 1 minute 30 seconds of video.

## 🎵 Audio Download Examples

### Extract Audio (Best Quality)
```
--extract-audio
```
Extracts audio in best available format.

### Extract Audio as MP3
```
--extract-audio --audio-format mp3
```
Extracts audio and converts to MP3.

### Extract Audio as M4A
```
--extract-audio --audio-format m4a
```
Extracts audio and converts to M4A.

### Audio Quality 320kbps
```
--extract-audio --audio-format mp3 --audio-quality 0
```
Best quality MP3 (320kbps).

### Audio Quality 128kbps
```
--extract-audio --audio-format mp3 --audio-quality 5
```
Medium quality MP3 (128kbps).

## 📝 Subtitle/CC Examples

### Download Subtitles
```
--write-subs
```
Downloads available subtitles.

### Download Auto-generated Subs
```
--write-auto-subs
```
Downloads auto-generated subtitles.

### Subtitles Only (Skip Video)
```
--write-subs --skip-download
```
Only downloads subtitles, no video.

### All Subtitles
```
--all-subs
```
Downloads all available subtitles.

## 📋 Information & List Examples

### List Available Formats
```
--list-formats
```
Shows all available video/audio formats.

### List Thumbnails
```
--list-thumbnails
```
Shows available thumbnail images.

### Get Video Info Only
```
--dump-json
```
Outputs full video metadata as JSON.

### Get Video URL Only
```
--get-url
```
Outputs the direct streaming URL.

## 🎥 Playlist Examples

### Download Entire Playlist
```
--yes-playlist
```
Downloads all videos in the playlist.

### Download First 5 Videos from Playlist
```
--yes-playlist --playlist-end 5
```
Downloads only first 5 videos.

### Download Playlist Items 3-7
```
--yes-playlist --playlist-start 3 --playlist-end 7
```
Downloads videos 3 to 7 from playlist.

### Reverse Playlist Order
```
--yes-playlist --playlist-reverse
```
Downloads playlist in reverse order.

## 🔧 Advanced Examples

### Custom Output Filename
```
-o "downloads/%(title)s.%(ext)s"
```
Note: The app already sets output directory, so you can just specify filename format.

### Embed Subtitles
```
--embed-subs
```
Embeds subtitles into the video file.

### Embed Thumbnails
```
--embed-thumbnail
```
Embeds thumbnail into video file (MP4/MKV/WEBM).

### Download Thumbnail Only
```
--write-thumbnail --skip-download
```
Only downloads the thumbnail image.

### Limit Download Speed
```
--limit-rate 1M
```
Limits download speed to 1MB/s.

### Continue Interrupted Downloads
```
--continue
```
Continues partially downloaded files.

### No Multipart (Single Connection)
```
--concurrent-fragments 1
```
Uses single connection for downloading.

### Retry on Failure
```
--retries 10
```
Retries up to 10 times on failure.

## 🔒 Authentication Examples

### Username & Password
```
--username USER --password PASS
```
For sites requiring login.

### Video Password
```
--video-password PASSWORD
```
For password-protected videos.

### Cookies from Browser
```
--cookies cookies.txt
```
Uses cookies from a cookies.txt file.

### Two-Factor Auth
```
--twofactor CODE
```
Provides 2FA code if needed.

## 🎨 Format Selection Examples

### MP4 Only
```
-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
```
Prefers MP4 format.

### WebM Only
```
-f "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best"
```
Prefers WebM format.

### Video Only (No Audio)
```
-f "bestvideo"
```
Downloads only video stream.

### Audio Only (No Video)
```
-f "bestaudio"
```
Downloads only audio stream.

### Max File Size 100MB
```
-f "best[filesize<100M]"
```
Downloads best quality under 100MB.

### Min Resolution 1080p
```
-f "best[height>=1080]"
```
Downloads 1080p or higher.

## 🌐 Network Examples

### Use Proxy
```
--proxy socks5://127.0.0.1:1080
```
Routes download through proxy.

### User Agent Spoof
```
--user-agent "Mozilla/5.0 ..."
```
Sets custom user agent.

### Referer
```
--referer "https://example.com"
```
Sets custom referer header.

### No Check Certificate
```
--no-check-certificate
```
Skips SSL certificate verification.

## 📁 Archive Examples

### Archive File (Track Downloaded)
```
--download-archive archive.txt
```
Tracks downloaded videos to avoid duplicates.

### Skip Already Downloaded
```
--download-archive archive.txt --no-overwrites
```
Skips files already in archive.

## 🎯 n8n Integration Examples

### Download Video Segment
```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "args": "--download-sections *00:00:10-00:01:30"
}
```

### Extract MP3
```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "args": "--extract-audio --audio-format mp3"
}
```

### Download Best Quality
```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "args": "-f bestvideo+bestaudio --merge-output-format mp4"
}
```

### Get Video Info Only
```json
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "args": "--dump-json"
}
```

### Download Playlist (First 3)
```json
{
  "url": "https://youtube.com/playlist?list=PLAYLIST_ID",
  "args": "--yes-playlist --playlist-end 3"
}
```

## 📚 Full Documentation

For complete options and examples, visit:
- **GitHub**: https://github.com/yt-dlp/yt-dlp
- **ReadTheDocs**: https://yt-dlp.readthedocs.io/
- **Chat with yt-dlp**: Run `yt-dlp --help` in terminal

## 💡 Tips

1. **Combine Options**: You can combine multiple options:
   ```
   --extract-audio --audio-format mp3 --audio-quality 0
   ```

2. **Quote Arguments**: If arguments have spaces, wrap in quotes when using API:
   ```json
   {
     "args": "-f \"bestvideo[ext=mp4]+bestaudio[ext=m4a]\""
   }
   ```

3. **Test First**: Use `--list-formats` to see available formats before downloading.

4. **Segment Format**: `*START-END` or `*START-+DURATION`:
   - `*00:00:10-00:01:30` → from 10s to 90s
   - `*00:00:10-+00:01:00` → from 10s for 60 seconds
   - `*-00:01:00` → last 60 seconds
