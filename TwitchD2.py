import os
import youtube_dl

def download_twitch_video(video_url, save_path):
    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)
    
    # Define options for youtube-dl with aria2c for faster downloading
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),
        'format': 'best',
        'external_downloader': 'aria2c',
        'external_downloader_args': ['-x', '16', '-s', '16', '-k', '1M', '-j', '16']
    }
    
    # Download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Example usage
video_url = "https://www.twitch.tv/videos/2169442247"
save_path = r"D:\TEST 2\Data\Pinterest\Twitch"
download_twitch_video(video_url, save_path)
