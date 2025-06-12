# Whisper Audio Transcription API

A robust and scalable FastAPI-based API for transcribing and translating audio files using OpenAI's Whisper model. This project provides a professional-grade solution for processing audio files, with support for multiple audio formats, model sizes, and tasks (transcription and translation).

## Table of Contents

- Features
- Requirements
- Installation
- Configuration
- Running the API
- API Endpoints
  - Health Check
  - Transcribe Audio
- Usage Examples
- Logging
- Project Structure
- Error Handling
- Performance Considerations
- Contributing
- License

## Features

- **FastAPI Framework**: Leverages FastAPI for high-performance, asynchronous API operations.
- **Whisper Integration**: Uses OpenAI's Whisper model for accurate audio transcription and translation.
- **Multiple Model Support**: Supports various Whisper model sizes (`tiny`, `base`, `small`, `medium`, `large`).
- **Task Flexibility**: Supports both transcription and translation tasks.
- **File Validation**: Validates audio file types (`.wav`, `.mp3`, `.m4a`, `.flac`) and enforces a 100MB file size limit.
- **GPU/CPU Support**: Automatically detects and utilizes CUDA for GPU acceleration if available.
- **Robust Logging**: Comprehensive logging to both console and file for debugging and monitoring.
- **Temporary File Management**: Secure handling and cleanup of temporary files.
- **Detailed Responses**: Includes processing time, model used, and language in API responses.
- **Swagger Documentation**: Auto-generated API documentation available at `/docs`.

## Requirements

- Python 3.8+
- FFmpeg (installed and accessible in system PATH)
- Dependencies (listed in `requirements.txt`):
  - `fastapi`
  - `uvicorn`
  - `whisper`
  - `torch`
  - `pydantic`
  - `pyyaml`

## Installation

1. \*\*Clone the Repository
