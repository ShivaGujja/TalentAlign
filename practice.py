from google import genai
import os
from google.genai import types

client =  genai.Client(api_key=os.getenv("MY_GEMINI_API"))

response = client.models.generate_content_stream(
    model="gemini-2.5-flash", contents="sum of  first five natural numberss",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=200) # Disables thinking
    ),
    

)
for stream in response:
    print(stream.text)