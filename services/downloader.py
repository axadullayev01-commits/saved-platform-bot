import yt_dlp
import asyncio
import os
import uuid

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def _download_media(url: str, extract_audio: bool = False) -> dict:
    unique_id = str(uuid.uuid4())
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/{unique_id}_%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    
    if extract_audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{DOWNLOAD_DIR}/{unique_id}_%(title)s.%(ext)s',
        })
    else:
        # Default to best quality
        ydl_opts.update({
            'format': 'best',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        if extract_audio:
            # When audio is extracted, yt-dlp might change the extension to mp3
            filename = os.path.splitext(filename)[0] + '.mp3'
            
        return {
            "title": info_dict.get('title', 'No title'),
            "description": info_dict.get('description', ''),
            "type": "audio" if extract_audio else ("photo" if info_dict.get('ext') in ['jpg', 'png', 'jpeg', 'webp'] else "video"),
            "file_path": filename
        }

async def download_media_async(url: str, extract_audio: bool = False) -> dict:
    """Run yt-dlp in a separate thread to avoid blocking the event loop."""
    return await asyncio.to_thread(_download_media, url, extract_audio)
