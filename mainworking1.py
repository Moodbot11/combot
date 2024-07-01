from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load the environment variables from .env file

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

class UserInput(BaseModel):
    user_input: str

@app.post("/chat/")
async def chat(input_data: UserInput):
    try:
        response = client.completions.create(
            engine="gpt-4-0613",  # Make sure this is the correct model
            prompt=input_data.user_input,
            max_tokens=150
        )
        
        if response.choices:
            response_text = response.choices[0].text.strip()
            finish_reason = response.choices[0].finish_reason
            return {"response": response_text, "finish_reason": finish_reason}
        else:
            return {"response": "", "finish_reason": "No response generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
