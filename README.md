# ComicCraft

ComicCraft is an AI-powered web application that creates a five-panel comic from a user prompt.

It uses:

- FastAPI backend
- Jinja2 HTML templates
- Gemini-compatible story generation
- Optional Hugging Face image generation
- Local placeholder images for offline mode
- FPDF2 PDF export

## Features

- Generates a complete five-panel comic story
- Creates panel titles, scenes, captions, narration, and dialogue
- Generates one image per panel
- Displays the comic in the browser
- Exports the comic as a PDF
- Supports a JSON API
- Runs without API keys in offline mode
- Supports Gemini and Hugging Face when API keys are configured

## Installation

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Copy the environment file:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Open:

- Application: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## Offline Mode

The default `.env` setting is:

```env
IMAGE_PROVIDER=placeholder
GEMINI_API_KEY=
```

This works without paid services, API keys, GPU installation, Stable Diffusion, or PyTorch.

## Gemini Mode

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
IMAGE_PROVIDER=placeholder
```

## Hugging Face Image Mode

To generate AI images using Hugging Face:

```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
IMAGE_PROVIDER=huggingface
HF_IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

## Run Tests

```bash
pytest
```