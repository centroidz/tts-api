from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import edge_tts
import tempfile
import os

app = FastAPI()

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text")
    voice = data.get("voice", "en-US-GuyNeural")

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(temp_path)

    def iterfile():
        with open(temp_path, "rb") as audio_file:
            yield from audio_file
        os.remove(temp_path)

    return StreamingResponse(iterfile(), media_type="audio/mpeg", headers={
        "Content-Disposition": "attachment; filename=speech.mp3"
    })
