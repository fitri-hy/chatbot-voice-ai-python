import requests
import pygame
from gtts import gTTS
import os

def get_gemini_response(question):
    url = f"https://api.hy-tech.my.id/api/gemini/{question}"
    response = requests.get(url)
    data = response.json()
    return data.get("text", "Sorry, I couldn't find the answer.")

def speak(text):
    tts = gTTS(text=text, lang='id') # lang voice
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("output.mp3")

def main():
    while True:
        try:
            question = input("Ask Something: ")
            if question.lower() == 'exit':
                break
            response_text = get_gemini_response(question)
            print("Answer (text):", response_text)
            speak(response_text)
        except KeyboardInterrupt:
            print("\nCanceled.")
            break
        except Exception as e:
            print("There is an error:", e)
            print("Sorry, an error occurred. Please try again.")

if __name__ == "__main__":
    main()
