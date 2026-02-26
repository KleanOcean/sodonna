"""Standalone test: generate an image with gemini-3-pro-image-preview."""

import json
from pathlib import Path

from google import genai
from google.genai import types

# Load API key from ~/.nanobot/config.json
config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
api_key = config["providers"]["gemini"]["apiKey"]

prompt = input("Enter image prompt (or Enter for default): ").strip()
if not prompt:
    prompt = "A cute orange cat sitting on a windowsill"

print(f"Generating: {prompt!r} ...")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"],
    ),
)

out_dir = Path.home() / ".nanobot" / "images"
out_dir.mkdir(parents=True, exist_ok=True)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(f"Text: {part.text}")
    elif part.inline_data is not None:
        from datetime import datetime
        path = out_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path.write_bytes(part.inline_data.data)
        print(f"Saved: {path} ({len(part.inline_data.data)} bytes)")
