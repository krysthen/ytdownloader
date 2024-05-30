import os
import tkinter as tk
from tkinter import messagebox, ttk
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def create_download_folder():
    desktop_path = get_desktop_path()
    download_folder = os.path.join(desktop_path, 'YouTube Downloads')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    return download_folder

def download_youtube_video(url, output_path, progress_var):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download(output_path=output_path, filename='video.mp4')
        progress_var.set(50)  # Ustawiamy postęp na 50% po pobraniu wideo
        
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(output_path=output_path, filename='audio.mp3')
        progress_var.set(100)  # Ustawiamy postęp na 100% po pobraniu audio
        
        return video_path, audio_path
    except Exception as e:
        return None, str(e)

def merge_video_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec='libx264')

def on_download():
    url = url_entry.get()
    output_path = create_download_folder()
    if not url:
        messagebox.showerror("Error", "URL cannot be empty.")
        return
    
    progress_var.set(0)  # Resetujemy postęp
    try:
        video_path, audio_path = download_youtube_video(url, output_path, progress_var)
        if video_path and audio_path:
            output_file_path = os.path.join(output_path, 'output.mp4')
            merge_video_audio(video_path, audio_path, output_file_path)
            messagebox.showinfo("Success", "Download completed successfully.")
        else:
            messagebox.showerror("Error", "Failed to download video.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Downloader")
root.geometry("380x180")
root.configure(bg='#171717')
root.resizable(False, False)

url_label = tk.Label(root, text="YouTube URL:", bg='#171717', fg='#676767')
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

url_entry = tk.Entry(root, width=59, bg='#2f2f2f', fg='#676767', borderwidth=0)
url_entry.grid(row=1, column=0, padx=10, pady=0, sticky='w')

download_button = tk.Button(root, width=50, text="Download", command=on_download, bg='#2f2f2f', fg='#ECECEC', borderwidth=0)
download_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

url_label = tk.Label(root, text="Progress:", bg='#171717', fg='#676767')
url_label.grid(row=3, column=0, padx=10, pady=0, sticky='w')

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, length=360, mode='determinate', variable=progress_var)
progress_bar.grid(row=4, column=0, padx=10, pady=0, sticky='w')

file_type_label = tk.Label(root, text="Made by krysthen.pl", bg='#171717', fg='#676767')
file_type_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')

root.mainloop()
