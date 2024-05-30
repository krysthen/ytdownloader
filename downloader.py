import os
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def create_download_folder():
    desktop_path = get_desktop_path()
    download_folder = os.path.join(desktop_path, 'YouTube Downloads')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    return download_folder

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=output_path)
        return yt.title
    except Exception as e:
        return str(e)

def on_download():
    url = url_entry.get()
    output_path = create_download_folder()
    if not url:
        messagebox.showerror("Error", "URL nie może być pusty.")
        return

    try:
        video_title = download_youtube_video(url, output_path)
        messagebox.showinfo("Sukces!", f"Pobrano: {video_title}, plik znajduje się na pulpicie!")
    except Exception as e:
        messagebox.showerror("Błąd", f"An error occurred: {e}")

root = tk.Tk()
root.title("Downloader")
root.geometry("380x140")
root.configure(bg='#171717')
root.resizable(False, False)

url_label = tk.Label(root, text="YouTube URL:", bg='#171717', fg='#ECECEC')
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

url_entry = tk.Entry(root, width=59, bg='#2f2f2f', fg='#ECECEC', borderwidth=0)
url_entry.grid(row=1, column=0, padx=10, pady=0, sticky='w')

download_button = tk.Button(root, width=50, text="Pobierz", command=on_download, bg='#2f2f2f', fg='#ECECEC', borderwidth=0)
download_button.grid(row=3, column=0, padx=10, pady=20, sticky='w')

root.mainloop()
