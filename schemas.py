from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000,
    )

    character_name: str = Field(
        default="Alex",
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        default="enchanted forest",
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        default="dramatic",
        max_length=40,
    )

    art_style: str = Field(
        default="comic book",
        max_length=80,
    )


class Panel(BaseModel):
    number: int
    title: str
    scene_description: str
    image_prompt: str

    caption: str = ""
    narration: str = ""
    dialogue: str = ""

    image_url: str = ""


class ComicResponse(BaseModel):
    title: str
    panels: list[Panel]
    pdf_url: str