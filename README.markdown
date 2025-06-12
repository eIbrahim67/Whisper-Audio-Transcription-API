# Audio Transcription API

A robust and scalable FastAPI-based API for transcribing and translating audio files using OpenAI's Whisper model. This project provides a professional-grade solution for processing audio files with features like file validation, performance tracking, and comprehensive logging.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Logging](#logging)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Audio Transcription and Translation**: Supports transcription and translation of audio files using OpenAI's Whisper models (`tiny`, `base`, `small`, `medium`, `large`).
- **File Validation**: Restricts uploads to supported audio formats (`.wav`, `.mp3`, `.m4a`, `.flac`) with a maximum file size of 100MB.
- **Performance Optimization**: Utilizes model caching with `@lru_cache` and GPU acceleration (CUDA) when available.
- **Comprehensive Logging**: Logs to both console and file (`transcription_api.log`) for debugging and monitoring.
- **Robust Error Handling**: Detailed error messages and proper cleanup of temporary files.
- **Performance Metrics**: Tracks processing time for transcription and overall request handling.
- **Structured Configuration**: Centralized configuration for easy maintenance.
- **Health Check Endpoint**: Provides API status, version, and hardware information.
- **FastAPI Documentation**: Interactive API documentation available at `/docs` and `/redoc`.

## Prerequisites

- **Python**: 3.8 or higher
- **FFmpeg**: Required for audio processing with Whisper
- **Dependencies**:
  - `fastapi`
  - `uvicorn`
  - `whisper` (OpenAI's Whisper library)
  - `torch` (with CUDA support for GPU acceleration, if available)
  - `pydantic`
  - `pyyaml`
- **Operating System**: Windows, macOS, or Linux (Windows-specific FFmpeg path in default config)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/audio-transcription-api.git
   cd audio-transcription-api
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn whisper torch pydantic pyyaml
   ```

4. **Install FFmpeg**:
   - **Windows**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and extract it to `C:\ffmpeg\bin`. Ensure the path matches the `FFMPEG_PATH` in the configuration.
   - **macOS**: Install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - **Linux**: Install via package manager:
     ```bash
     sudo apt-get install ffmpeg  # Debian/Ubuntu
     sudo yum install ffmpeg      # CentOS/RHEL
     ```

5. **Verify FFmpeg Installation**:
   ```bash
   ffmpeg -version
   ```

## Configuration

The application uses a configuration dictionary in `main.py`. Key settings include:

- `FFMPEG_PATH`: Path to FFmpeg binary (default: `C:\ffmpeg\bin`)
- `ALLOWED_EXTENSIONS`: Supported audio formats (`.wav`, `.mp3`, `.m4a`, `.flac`)
- `VALID_MODELS`: Whisper model sizes (`tiny`, `base`, `small`, `medium`, `large`)
- `VALID_TASKS`: Supported tasks (`transcribe`, `translate`)
- `MAX_FILE_SIZE`: Maximum upload size (100MB)
- `LOG_LEVEL`: Logging level (`INFO`, `DEBUG`, etc.)
- `HOST` and `PORT`: Server host (`0.0.0.0`) and port (`8000`)

To customize, modify the `CONFIG` dictionary in `main.py`. Future versions may support a separate YAML configuration file.

## Running the Application

1. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Server**:
   ```bash
   python main.py
   ```

   The server will start on `http://0.0.0.0:8000` with auto-reload enabled for development.

3. **Access Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### `GET /health`
- **Description**: Check the API's health status.
- **Response**:
  ```json
  {
    "status": "ok",
    "version": "2.0.0",
    "cuda_available": true
  }
  ```

### `POST /transcribe`
- **Description**: Transcribe or translate an uploaded audio file.
- **Parameters**:
  - `file` (UploadFile): Audio file (`.wav`, `.mp3`, `.m4a`, `.flac`)
  - `language` (str, optional): Language code (e.g., `en` for English, default: `en`)
  - `model_size` (str, optional): Whisper model size (`tiny`, `base`, `small`, `medium`, `large`, default: `small`)
  - `task` (str, optional): Task type (`transcribe` or `translate`, default: `transcribe`)
- **Response**:
  ```json
  {
    "status": "success",
    "transcribed_text": "Transcribed audio text here",
    "error": null,
    "processing_time": 2.45,
    "model_used": "small",
    "language": "en"
  }
  ```
- **Error Response**:
  ```json
  {
    "status": "error",
    "transcribed_text": null,
    "error": "Unsupported file type: .ogg",
    "processing_time": 0.12,
    "model_used": "small",
    "language": "en"
  }
  ```

## Usage Examples

### Using `curl`
```bash
curl -X POST "http://localhost:8000/transcribe?language=en&model_size=small&task=transcribe" \
  -F "file=@sample.wav" \
  -H "Content-Type: multipart/form-data"
```

### Using Python (`requests`)
```python
import requests

url = "http://localhost:8000/transcribe"
files = {"file": open("sample.wav", "rb")}
params = {"language": "en", "model_size": "small", "task": "transcribe"}
response = requests.post(url, files=files, params=params)
print(response.json())
```

### Testing with Swagger UI
1. Open `http://localhost:8000/docs` in your browser.
2. Select the `POST /transcribe` endpoint.
3. Upload an audio file and specify parameters.
4. Execute the request and view the response.

## Logging

Logs are written to:
- Console (stdout)
- File (`transcription_api.log`)

Log entries include:
- Timestamp
- Logger name
- Log level
- Message

Example log entry:
```
2025-06-12 03:15:23,456 - main - INFO - Starting transcription for file: sample.wav
```

To change the log level, modify `CONFIG["LOG_LEVEL"]` in `main.py`.

## Project Structure

```
audio-transcription-api/
├── main.py                 # Main application code
├── temp_files/             # Temporary directory for uploaded files
├── transcription_api.log   # Log file
├── venv/                   # Virtual environment
├── README.md               # This file
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows PEP 8 and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact:
- **Email**: your.email@example.com
- **GitHub Issues**: [github.com/your-username/audio-transcription-api/issues](https://github.com/your-username/audio-transcription-api/issues)
