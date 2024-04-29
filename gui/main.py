import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import requests
import pygame
from gtts import gTTS
import os
import threading

is_playing = False

def get_gemini_response(question):
    url = f"https://api.hy-tech.my.id/api/gemini/{question}"
    response = requests.get(url)
    data = response.json()
    return data.get("text", "Sorry, I couldn't find the explanation.")

def speak(text):
    global is_playing
    is_playing = True

    tts = gTTS(text=text, lang='id') # lang voice
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() and is_playing:
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("output.mp3")

def on_ask():
    global is_playing
    if not is_playing:
        question = entry.get()
        response = get_gemini_response(question)
        response_label.config(text=response)
        threading.Thread(target=speak, args=(response,)).start()

def on_cancel():
    global is_playing
    if is_playing:
        is_playing = False

root = tk.Tk()
root.title("Voice AI Response")

style = ThemedStyle(root)
style.set_theme("equilux")

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.grid(row=0, column=0, sticky="nsew")

label = ttk.Label(main_frame, text="Ask Something:")
label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry = ttk.Entry(main_frame, width=40)
entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

ask_button = ttk.Button(main_frame, text="Ask", command=on_ask)
ask_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

response_label = ttk.Label(main_frame, text="")
response_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

cancel_button = ttk.Button(main_frame, text="Cancelled", command=on_cancel)
cancel_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

root.mainloop()