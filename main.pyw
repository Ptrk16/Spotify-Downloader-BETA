import tkinter.filedialog
from tkinter import *
import os
import os.path


# Frame Settings
root = Tk()
root.title("Spotify Downloader")
root.geometry("500x220")

try:
    root.iconbitmap(os.getcwd() + "\\favicon.ico")
except:
    pass

# URL Hint
hint = Label(root, text="Song / Playlist URL or Name:", font='Helvetica 9')
hint.pack(pady=10)

# URL Field
e = Entry(root, width=70, bg="wheat", fg="black")
e.pack(pady=0)

# Formats
options = [
    "Choose format",
    "flac",
    "mp3",
    "ogg",
    "m4a",
    "wav",
    "opus"
]
clicked = StringVar()
clicked.set(options[0])
drop = OptionMenu(root, clicked, *options)
drop.pack(pady=10)


def read_location():
    if os.path.isfile("download-location.txt"):
        with open("download-location.txt") as file:
            location = file.read().rstrip()
        if not os.path.isdir(location):
            user = os.environ["USERPROFILE"]
            location = f"{user}\\Downloads"
            with open("download-location.txt", "w") as file:
                file.write(location)
    else:
        user = os.environ["USERPROFILE"]
        location = f"{user}\\Downloads"
        with open("download-location.txt", "w") as file:
            file.write(location)

    return location


def change_location():
    changed_location = tkinter.filedialog.askdirectory()
    changed_location = changed_location.replace("/", "\\")
    if len(changed_location) != 0:
        with open('download-location.txt', 'w') as f:
            f.write(changed_location)
    change_download_location.config(text=f"Change current download location?:\n{read_location()}")


def download():
    url = e.get()
    output_format = clicked.get()
    if url and output_format != "Choose format":  #
        location = read_location()
        os.system(f"cmd /c spotdl \"{url}\" --output-format {output_format} --output \"{location}\" --ignore-ffmpeg-version --lyrics-provider genius")
        try:
            os.remove(f"{location}\\.spotdl-cache")
        except:
            pass


# Download Button
startDownload = Button(root, text="Download", command=lambda: [download()], bg="lime", font='Helvetica 9 bold')
startDownload.pack()

# Change Download Location Button
change_download_location = Button(root, text=f"Change current download location?:\n{read_location()}", font='Helvetica 9', command=lambda: [change_location()])
change_download_location.pack(pady=20)

root.mainloop()
