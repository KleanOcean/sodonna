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

# Consistency anchor — included in every Donna prompt
DONNA_ANCHOR = (
    "A professional woman in her mid-30s with auburn-brown hair pulled back in a low bun, "
    "wearing a dark fitted blazer over a simple cream top. Natural makeup, warm complexion, "
    "light freckles. Modern dark office setting with warm desk-lamp lighting."
)

IMAGES = [
    {
        "name": "hero_donna.png",
        "prompt": (
            f"Photorealistic editorial photograph. {DONNA_ANCHOR} "
            "She is seated at a sleek dark desk, typing on a MacBook laptop. A warm brass "
            "desk lamp illuminates her face from the side. A ceramic coffee cup sits nearby. "
            "Behind her, floor-to-ceiling windows show a blurred city skyline at dusk (bokeh "
            "lights). Shot from a 3/4 angle showing her from the waist up. She has a focused, "
            "confident expression — in her element. Portrait format, 800x1000 aspect ratio. "
            "Warm cinematic color grading. No text."
        ),
    },
    {
        "name": "donna_painpoints.png",
        "prompt": (
            f"Photorealistic editorial photograph. {DONNA_ANCHOR} "
            "She is sitting at her desk looking overwhelmed — multiple browser tabs visible on "
            "two monitors, sticky notes scattered everywhere, phone buzzing beside her. She is "
            "rubbing her temples with her eyes closed, stressed expression. Papers and notebooks "
            "are spread across the desk chaotically. The warm desk lamp still lights the scene "
            "but the mood feels heavier. This is the 'before' moment — drowning in busywork. "
            "Wide cinematic format, 1200x500 aspect ratio. Warm color grading. No text."
        ),
    },
    {
        "name": "donna_features.png",
        "prompt": (
            f"Photorealistic editorial photograph. {DONNA_ANCHOR} "
            "She is standing confidently at a large glass whiteboard in her office, drawing a "
            "workflow diagram with a blue marker. She has a confident, knowing smile — she has "
            "the plan. The whiteboard shows connected boxes and arrows (a strategic workflow). "
            "Warm desk lamp and ambient office lighting. She is turned slightly toward the "
            "camera, marker in right hand. This is the 'strategic planning' moment — everything "
            "organized. Wide cinematic format, 1200x500 aspect ratio. Warm color grading. No text."
        ),
    },
    {
        "name": "donna_philosophy.png",
        "prompt": (
            f"Photorealistic editorial photograph. {DONNA_ANCHOR} "
            "She is sitting back in her office chair, laptop open on the desk in front of her, "
            "looking relaxed and satisfied with a calm confident smile. Golden hour sunlight "
            "streams through the window behind her, creating a warm halo. Her posture is open "
            "and at ease — everything is under control. One hand rests on the chair arm. The "
            "mood is 'mission accomplished'. Wide cinematic format, 1200x600 aspect ratio. "
            "Warm golden color grading. No text."
        ),
    },
    {
        "name": "donna_footer.png",
        "prompt": (
            f"Photorealistic editorial close-up portrait. {DONNA_ANCHOR} "
            "Cropped from shoulders up. She is looking directly at the camera with a knowing "
            "half-smile — the look of someone who already has all the answers. Warm desk-lamp "
            "lighting illuminates her face from the side, creating soft shadows. Dark office "
            "background blurred out. Shallow depth of field. Intimate, powerful portrait. "
            "800x500 aspect ratio. Warm cinematic color grading. No text."
        ),
    },
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
