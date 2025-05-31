import os
import youtube_dl
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import sys

class RedirectText(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

def download_twitch_video(video_url, save_path):
    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)
    
    # Define options for youtube-dl with aria2c for faster downloading
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),
        'format': 'best',
        'external_downloader': 'aria2c',
        'external_downloader_args': ['-x', '16', '-s', '16', '-k', '1M', '-j', '16'],
        'progress_hooks': [progress_hook]
    }
    
    # Download the video
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, folder_selected)

def start_download():
    video_url = url_entry.get()
    save_path = save_path_entry.get()
    if video_url and save_path:
        # Redirect stdout to the console text widget
        sys.stdout = RedirectText(console_text)
        # Start the download in a new thread to keep the GUI responsive
        threading.Thread(target=download_twitch_video, args=(video_url, save_path)).start()
    else:
        messagebox.showwarning("Input required", "Please provide both video URL and save path.")

def progress_hook(d):
    if d['status'] == 'downloading':
        console_text.insert(tk.END, f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA: {d['_eta_str']}\n")
        console_text.see(tk.END)
    elif d['status'] == 'finished':
        console_text.insert(tk.END, 'Download complete!\n')
        console_text.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Twitch Video Downloader")

# Create and place labels, entries, and buttons
tk.Label(root, text="Twitch Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Save Path:").grid(row=1, column=0, padx=10, pady=10)
save_path_entry = tk.Entry(root, width=50)
save_path_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=10, pady=10)

download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=1, pady=20)

# Create a scrolled text widget for the console log
console_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
console_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
