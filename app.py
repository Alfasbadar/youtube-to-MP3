import tkinter as tk
from tkinter import Tk, filedialog
from threading import Thread
import io
import os
import customtkinter
from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
import warnings
from PIL import Image, ImageTk
from tqdm import tqdm


def hide_ffmpeg_warning():
    # Hide FFmpeg warning
    warnings.filterwarnings("ignore", category=UserWarning, module="pydub")

# Call the function to hide FFmpeg warning
hide_ffmpeg_warning()

def search_youtube(keyword):
    try:
        # Perform a YouTube search
        videos_search = VideosSearch(keyword, limit=1)
        results = videos_search.result()

        # Extract relevant information from the search results
        video_info = results['result'][0] if results['result'] else None

        if video_info:
            # Extract desired parameters
            title = video_info['title']
            duration = video_info.get('duration', 'Unknown Duration')
            thumbnail = video_info.get('thumbnails', [{}])[0].get('url', 'No Thumbnail')

            # Get the video URL using video ID
            video_id = video_info.get('id', 'No ID')
            link = f'https://www.youtube.com/watch?v={video_id}'

            # Return a tuple with the extracted information
            return link, thumbnail, title, duration
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def on_submit():
    button.configure(text="Downloading...",state=tk.DISABLED)
    # show the progressbar
    global keyword
    global audiodata  # Declare audiodata as global
    keyword = entry.get()
    if keyword == "":
        entry.configure(placeholder_text="Not found")
        downLabel.pack_forget()
        button.configure(text="Download",state=tk.ACTIVE)
        frame.pack_forget()
        return

    # Start a new thread for downloading audio
    Thread(target=download_audio, daemon=True).start()

def download_audio():
    global keyword
    global audiodata
    result = search_youtube(keyword + " song")
    frame.pack()
    if result:
        url, image, title, duration = result
        button.pack_forget()
        print(f"Video URL: {url}")
        print(f"Thumbnail URL: {image}")
        print(f"Title: {title}")
        print(f"Duration: {duration}")
        button2.pack(pady=10)
        label3.configure(text=title)
        label2.configure(text="Duration : " + duration)
        label1.configure(text="Bitrate :" + " 320kbps")
        audiodata = get_youtube_audio(url)
    else:
        print(f"No results found for '{keyword}' on YouTube.")

def on_save():
    try:
        save_audio_to_file_with_windows_dialog(audiodata,title)  # Pass the global audiodata
    except Exception as e:
        print(f"An error occurred: {e}")

def save_audio_to_file_with_windows_dialog(audiodata,title):
    try:
        # Use filedialog to get the target folder from the user
        target_folder = filedialog.askdirectory()

        if not target_folder:
            print("Operation canceled by user.")
            return

        # Specify the file path (you can customize the file name if needed)
        file_path = os.path.join(target_folder, f"{title}.mp3")

        # Save the audio to the specified file path
        audiodata.seek(0)
        with open(file_path, "wb") as f:
            f.write(audiodata.read())

        print(f"Audio saved successfully at: {file_path}")
        resetapp()
    except Exception as e:
        print(f"An error occurred: {e}")
def resetapp():
    button2.pack_forget()
    frame.pack_forget()
    button.pack(pady=10)

def get_youtube_audio(url):
    try:
        # Download the best available YouTube audio stream
        youtube = YouTube(url)
        audio_stream = youtube.streams.filter(only_audio=True).first()

        # Load the audio content into a variable
        audio_content = io.BytesIO()
        audio_stream.stream_to_buffer(audio_content)
        audio_content.seek(0)

        return audio_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

root = customtkinter.CTk()
root.title("freemusic")

# Set the window icon
root.iconbitmap("icon.ico")

# Set the minimum size
root.minsize(700, 300)  # Adjust the values as needed

# Create and pack widgets
entry = customtkinter.CTkEntry(master=root,
                               placeholder_text="Search ... ",
                               width=300,
                               height=25,
                               border_width=2,
                               corner_radius=10)
entry.pack(pady=20, padx=20)

# Create and arrange four labels in the same row using grid
frame = customtkinter.CTkFrame(master=root, width=200, height=200)

label1 = customtkinter.CTkLabel(frame, text="Size", text_color="#0066ff", fg_color="transparent")
label1.pack(side=tk.BOTTOM, padx=20)

label2 = customtkinter.CTkLabel(frame, text="Duration", text_color="#0066ff", fg_color="transparent")
label2.pack(side=tk.BOTTOM, padx=20)

label3 = customtkinter.CTkLabel(frame, text="Bit rate", text_color="#0066ff", fg_color="transparent")
label3.pack(side=tk.BOTTOM, padx=20)

# Create and arrange four labels in the same row using grid
frame1 = customtkinter.CTkFrame(master=root, width=200, height=200, fg_color="transparent")

label4 = customtkinter.CTkLabel(frame1, text="Size", fg_color="transparent")
label4.pack(side=tk.LEFT, padx=20)

label5 = customtkinter.CTkLabel(frame1, text="Duration", fg_color="transparent")
label5.pack(side=tk.LEFT, padx=20)

label6 = customtkinter.CTkLabel(frame1, text="Bit rate", fg_color="transparent")
label6.pack(side=tk.LEFT, padx=20)

button = customtkinter.CTkButton(root, text="Download", command=on_submit)
button.pack(pady=10)


button2 = customtkinter.CTkButton(root, text="Save", command=on_save)

downLabel = customtkinter.CTkLabel(root, text="Downloading", fg_color="transparent")



# Bind the Enter key to the on_submit function
root.bind("<Return>", lambda event=None: on_submit())

# Main program
root.mainloop()
