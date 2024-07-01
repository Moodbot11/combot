from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load the environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("Chat with GPT-4 (type 'quit' to exit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        try:
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )

            print("GPT-4:", completion.choices[0].message.content.strip())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
