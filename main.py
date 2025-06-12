import os, logging, torch, uvicorn
import whisper
from functools import lru_cache
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

FFMPEG_PATH = r"C:\ffmpeg\bin"
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac'}
VALID_MODELS = {"tiny", "base", "small", "medium", "large"}
VALID_TASKS = {"transcribe", "translate"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Audio Transcription API",
    description="API for transcribing audio files using OpenAI's Whisper",
    version="1.1.0"
)

class TranscriptionResponse(BaseModel):
    transcribed_text: Optional[str]
    status: str
    error: Optional[str]

def configure_environment():
    """Adds ffmpeg to system PATH."""
    os.environ["PATH"] += os.pathsep + FFMPEG_PATH
    logger.info("FFmpeg path configured.")

@lru_cache()
def get_model(model_size: str):
    """Loads the Whisper model once and caches it."""
    if model_size not in VALID_MODELS:
        raise ValueError(f"Invalid model size: {model_size}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Loading Whisper model '{model_size}' on {device}...")
    return whisper.load_model(model_size).to(device)

def transcribe_audio(model, file_path: str, language: str, task: str, fp16: bool):
    """Transcribes the audio using the Whisper model."""
    logger.info("Starting transcription...")
    return model.transcribe(file_path, language=language, task=task, fp16=fp16)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_endpoint(
    file: UploadFile = File(...),
    language: str = "en",
    model_size: str = "small",
    task: str = "transcribe"
):
    """Transcribes or translates an uploaded audio file."""
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}"
        )

    # Validate model and task
    if model_size not in VALID_MODELS:
        raise HTTPException(status_code=400, detail=f"Invalid model size. Choose from: {VALID_MODELS}")
    if task not in VALID_TASKS:
        raise HTTPException(status_code=400, detail=f"Invalid task. Choose from: {VALID_TASKS}")

    temp_file_path = f"temp_{file.filename}"
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        configure_environment()

        logger.info(f"Processing transcription for file: {file.filename}")
        model = get_model(model_size)
        fp16 = torch.cuda.is_available()

        result = transcribe_audio(model, temp_file_path, language, task, fp16)
        print(result)
        if not result or "text" not in result:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "error": "Transcription failed", "transcribed_text": None}
            )

        return TranscriptionResponse(
            status="success",
            transcribed_text=result["text"].strip(),
            error=None
        )

    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e), "transcribed_text": None}
        )
    # finally:
    #     if os.path.exists(temp_file_path):
    #         os.remove(temp_file_path)


# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)