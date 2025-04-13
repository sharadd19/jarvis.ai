from fastapi.responses import StreamingResponse
import google.generativeai as genai
import os


# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model instance
model = genai.GenerativeModel("gemini-2.0-flash")  # or "gemini-pro", "gemini-1.5-pro" as needed

async def stream(prompt: str):
    response = await model.generate_content_async(
        [prompt],
        stream=True)
        
    async def stream_chunks():
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    return StreamingResponse(stream_chunks())