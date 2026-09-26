from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage_loads():
    """
    Ensure homepage loads correctly.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_image_generation_endpoint():
    """
    Ensure local placeholder image generation endpoint works.
    """

    response = client.get(
        "/test-image",
        params={
            "prompt": "A superhero standing on a city rooftop",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "image_url" in data
    assert data["image_url"].startswith("/static/panels/")


def test_generate_comic_json():
    """
    Ensure JSON API returns a five-panel comic.
    """

    payload = {
        "prompt": "A brave fox explores an enchanted forest.",
        "character_name": "Fia",
        "setting": "enchanted forest",
        "tone": "funny",
        "art_style": "comic book",
    }

    response = client.post(
        "/generate-comic/json",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "title" in data
    assert "panels" in data
    assert "pdf_url" in data

    assert len(data["panels"]) == 5

    first_panel = data["panels"][0]

    assert first_panel["number"] == 1
    assert first_panel["title"]
    assert first_panel["scene_description"]
    assert first_panel["image_prompt"]
    assert first_panel["image_url"].startswith("/static/panels/")


def test_generate_comic_form():
    """
    Ensure HTML form-based comic generation works.
    """

    form_data = {
        "prompt": "A young inventor builds a flying bicycle.",
        "character_name": "Mira",
        "setting": "a busy city",
        "tone": "light-hearted",
        "art_style": "anime",
    }

    response = client.post(
        "/generate",
        data=form_data,
    )

    assert response.status_code == 200
    assert "Mira" in response.text
    assert "Download Comic PDF" in response.text