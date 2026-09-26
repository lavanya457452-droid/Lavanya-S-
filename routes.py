from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .schemas import PromptRequest
from .services.exporter import save_pdf
from .services.gemini import generate_panels
from .services.images import generate_image


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    """
    Display the ComicCraft homepage.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_from_form(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Alex"),
    setting: str = Form("enchanted forest"),
    tone: str = Form("dramatic"),
    art_style: str = Form("comic book"),
):
    """
    Create a comic after an HTML form submission.
    """

    try:
        data = PromptRequest(
            prompt=prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        comic = await build_comic(data)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "comic": comic,
            },
        )

    except Exception as error:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(error),
            },
            status_code=500,
        )


@router.post(
    "/generate-comic/json",
)
async def generate_from_json(
    data: PromptRequest,
):
    """
    Generate a comic through the JSON API.
    """

    try:
        return await build_comic(data)

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Comic generation failed: {error}",
        ) from error


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(request: Request):
    """
    Display the PDF export success page.
    """

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )


@router.get(
    "/test-image",
)
async def test_image(
    prompt: str = "A superhero standing on a city rooftop at sunset",
):
    """
    Generate and return a single test image.
    """

    image_url = await generate_image(
        prompt=prompt,
        number=0,
    )

    return {
        "prompt": prompt,
        "image_url": image_url,
    }


async def build_comic(
    data: PromptRequest,
) -> dict:
    """
    Full ComicCraft pipeline:
    1. Create story panels.
    2. Generate panel images.
    3. Export a PDF.
    4. Return the completed comic.
    """

    title, panels = await generate_panels(data)

    for panel in panels:
        panel_number = panel["number"]
        image_prompt = panel["image_prompt"]

        image_url = await generate_image(
            prompt=image_prompt,
            number=panel_number,
        )

        panel["image_url"] = image_url

    pdf_url = save_pdf(
        title=title,
        panels=panels,
    )

    return {
        "title": title,
        "panels": panels,
        "pdf_url": pdf_url,
    }