from typing import List

from pydantic import BaseModel, Field, PositiveInt


class GenerationParams(BaseModel):
    """Minimal parameters for Fooocus generation."""

    prompt: str
    negative_prompt: str = Field(default="")
    num_images: PositiveInt = Field(default=1)
    seed: str = Field(default="-1")
    styles: List[str] = Field(default_factory=lambda: []) #"Fooocus V2"
    performance: str = Field(default="Speed")
    aspect_ratio: str = Field(default="768×1280")
    output_format: str = Field(default="png")
    image_sharpness: int = Field(default=2, ge=0, le=30)
    guidance_scale: int = Field(default=4, ge=1, le=30)
    base_model: str = Field(default="hotart_5.safetensors")


