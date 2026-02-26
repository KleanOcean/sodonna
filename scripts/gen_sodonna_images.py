"""Generate SoDonna landing page images using Gemini image generation."""

import json
import time
from pathlib import Path

from google import genai
from google.genai import types

# Load API key
config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
api_key = config["providers"]["gemini"]["apiKey"]
client = genai.Client(api_key=api_key)

# Output directory
OUT_DIR = Path(__file__).resolve().parent.parent / "sodonna_webapp" / "public" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "name": "feature_brain.png",
        "prompt": (
            "Generate a dark premium UI mockup image: a knowledge base / note-taking "
            "application interface on a pure black (#09090B) background. Show glassmorphic "
            "cards with colorful tags (purple, blue, cyan pill-shaped labels), a search bar "
            "with a soft purple glow at the top, and floating note cards with blurred edges. "
            "Clean minimal SaaS aesthetic. The style should be polished, modern, and "
            "photorealistic UI design. Dark mode. 800x600 aspect ratio."
        ),
    },
    {
        "name": "feature_dashboard.png",
        "prompt": (
            "Generate a dark premium UI mockup image: an analytics dashboard on a pure "
            "black (#09090B) background. Show three metric cards (revenue, traffic, "
            "conversion) with glowing accent lines in purple, blue, and cyan. Include "
            "minimal charts with gradient area fills below the cards. Glassmorphic frosted "
            "semi-transparent panels. Executive dashboard style — clean, data-rich but not "
            "cluttered. Dark mode, modern SaaS aesthetic. 800x600 aspect ratio."
        ),
    },
    {
        "name": "feature_flow.png",
        "prompt": (
            "Generate a dark premium UI mockup image: an automation workflow visualization "
            "on a pure black (#09090B) background. Show connected nodes forming a horizontal "
            "flow with glowing gradient connection lines that go from purple to blue to cyan. "
            "Each node is a glassmorphic rounded rectangle with a simple icon inside. The flow "
            "shows content being distributed to multiple platform icons at the end. Dark mode, "
            "modern SaaS aesthetic, clean and minimal. 800x600 aspect ratio."
        ),
    },
    {
        "name": "hero_orb.png",
        "prompt": (
            "Generate an abstract 3D glass orb floating on a pure black background. The orb "
            "has purple-to-cyan gradient refraction and internal light caustics. It floats "
            "above a subtle dark reflective surface with soft reflection. Ethereal light rays "
            "emanate from behind. Ultra-minimal composition, cinematic lighting, no text "
            "anywhere. The image evokes intelligence and elegance. Photorealistic 3D render "
            "style. 1200x800 aspect ratio, wide format."
        ),
    },
]


def generate_image(name: str, prompt: str) -> bool:
    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"{'='*60}")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(f"  Model says: {part.text}")
        elif part.inline_data is not None:
            path = OUT_DIR / name
            path.write_bytes(part.inline_data.data)
            size_kb = len(part.inline_data.data) / 1024
            print(f"  Saved: {path} ({size_kb:.1f} KB)")
            return True

    print(f"  WARNING: No image data returned for {name}")
    return False


def main():
    print(f"Output directory: {OUT_DIR}")
    print(f"Generating {len(IMAGES)} images...\n")

    results = []
    for i, img in enumerate(IMAGES):
        success = generate_image(img["name"], img["prompt"])
        results.append((img["name"], success))

        # Rate limiting: wait between calls (skip after last)
        if i < len(IMAGES) - 1:
            print("  Waiting 5s (rate limit)...")
            time.sleep(5)

    print(f"\n{'='*60}")
    print("RESULTS:")
    for name, ok in results:
        status = "OK" if ok else "FAILED"
        print(f"  [{status}] {name}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
