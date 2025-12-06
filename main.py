from fastapi import FastAPI, Request, Response
import edge_tts
import tempfile
import asyncio
import os

app = FastAPI()

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text")
    voice = data.get("voice", "en-US-JennyNeural")

    if not text:
        return {"error": "Text is required"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(temp_path)

    with open(temp_path, "rb") as audio:
        audio_bytes = audio.read()

    os.remove(temp_path)

    return Response(content=audio_bytes, media_type="audio/mpeg")
