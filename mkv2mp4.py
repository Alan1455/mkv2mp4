#-*- coding: utf-8 -*-
# by tempuraaaa#0

import asyncio
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip

# gui
root = tk.Tk()
root.title("MKV to MP4 Converter")
root.iconphoto(False, tk.PhotoImage(file="./icon.png"))

window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

width = 600
height = 260
left = int((window_width - width) / 2)
top = int((window_height - height) / 2)
root.geometry(f"{width}x{height}+{left}+{top}")
root.resizable(0, 0)

# frame 1
frame1 = tk.LabelFrame(root, text="File name")
frame1.pack(side="top")
frame1.pack_propagate(False)

file_name = tk.StringVar()
file_name.set("file name: ")

path_label = tk.Label(frame1, textvariable=file_name, relief="solid", fg="black", width=50, font=("Arial", 11, "bold"))
path_label.grid(row=0, column=0, padx=5, pady=5)

file_path: str = None

def show():
    global file_path
    file_path = filedialog.askopenfilename()
    file_name.set(f"file name: {file_path.split('/')[-1]}")

btn = tk.Button(frame1, text="Open File", font=("Arial", 10, "bold"), command=show)
btn.grid(row=0, column=1, padx=5, pady=5)

# frame 2
frame2 = tk.LabelFrame(root, text="Output file name")
frame2.pack(pady=10)
frame2.pack_propagate(False)

new_file_name = tk.StringVar()
entry = tk.Entry(frame2, textvariable=new_file_name, fg="black", font=("Arial", 11))
entry.grid(row=0, column=0, padx=5, pady=5)

def clear():
    new_file_name.set("")

btnClear = tk.Button(frame2, text="Clear", font=("Arial", 10, "bold"), command=clear)
btnClear.grid(row=0, column=1, padx=5, pady=5)

# frame 3
frame3 = tk.LabelFrame(root, text="Convert options")
frame3.pack()
frame3.pack_propagate(False)

var = tk.StringVar(value="mkv2mp4")

def Selection():
    pass

rbmp4 = tk.Radiobutton(frame3, text="mkv to mp4", variable=var, value="mkv2mp4", command=Selection)
rbmp4.grid(row=0, column=0, padx=5, pady=5)

rbmp3 = tk.Radiobutton(frame3, text="mkv to mp3", variable=var, value="mkv2mp3", command=Selection)
rbmp3.grid(row=0, column=1, padx=5, pady=5)

# progress
progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress.pack(pady=5)

bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=5, pady=5)

status_label = tk.Label(bottom_frame, text="", anchor="w")
status_label.grid(row=0, column=0, sticky="w", padx=5)

convert_btn = tk.Button(bottom_frame, text="Convert", font=("Arial", 10, "bold"), command=lambda: asyncio.run(convert_async()))
convert_btn.grid(row=0, column=1, sticky="e", padx=5)

bottom_frame.grid_columnconfigure(0, weight=1)

def check_file():
    if not file_path:
        messagebox.showwarning("Error", "Oops! No file selected!")
        return False
    return file_path.endswith(".mkv")

def mkv2mp4(file: str, output_name: str):
    status_label.config(text="Currently processing: Converting (MKV -> MP4)")
    video = VideoFileClip(file)
    video.write_videofile(f"{output_name}.mp4", codec="mpeg4", audio_codec="aac")

def mkv2mp3(file: str, output_name: str):
    status_label.config(text="Currently processing: Converting (MKV -> MP3)")
    video = VideoFileClip(file)
    audio = video.audio
    audio.write_audiofile(f"{output_name}.mp3", codec="libmp3lame")

async def convert_async():
    if not check_file():
        return
    output_name = new_file_name.get().strip()
    if not output_name:
        messagebox.showwarning("Error", "Please enter an output file name!")
        return

    progress["value"] = 0
    status_label.config(text="Currently processing: Prepare for conversion...")

    def run():
        try:
            if var.get() == "mkv2mp4":
                mkv2mp4(file_path, output_name)
            elif var.get() == "mkv2mp3":
                mkv2mp3(file_path, output_name)
            progress["value"] = 100
            status_label.config(text="Currently processing: Finish ✅")
            messagebox.showinfo("Success", "Conversion complete!")
        except Exception as e:
            progress["value"] = 0
            status_label.config(text="Currently processing: Conversion failed ❌")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    root.mainloop()

