import os
import subprocess
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import openai

# Load the environment variables from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def listen():
    # Initialize the recognizer
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except Exception as e:
            print(f"Could not understand audio: {e}")
            return None

def speak(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(str(speech_file_path))
    subprocess.run(["afplay", str(speech_file_path)])

def main():
    print("Chat with GPT-4 (say 'quit' to exit)")

    while True:
        print("\nYou: ", end="")
        user_input = listen()

        if user_input is None or user_input.lower() == 'quit':
            break

        try:
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            response = completion.choices[0].message.content.strip()
            print("GPT-4:", response)
            speak(response)  # Bot speaks the response

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()