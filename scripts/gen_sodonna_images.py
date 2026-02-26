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
# This is an ORIGINAL character design, not based on any real person or copyrighted character.
DONNA_ANCHOR = (
    "A professional Caucasian woman in her early 30s with long auburn (copper-red) hair, "
    "loosely wavy, side-parted and falling past her shoulders. She wears a dark fitted suit "
    "(black or deep navy) over a black V-neck top. Fair skin with light freckles, "
    "blue-green eyes, sculpted features. Polished but natural makeup with a dewy finish. "
    "She radiates effortless authority — confident, composed, in total command. "
    "Modern dark-toned office or law-firm aesthetic, warm brass desk-lamp as key light."
)

IMAGES = [
    # --- Donna character images (4) ---
    {
        "name": "hero_donna.png",
        "prompt": (
            f"Photorealistic editorial photograph. {DONNA_ANCHOR} "
            "She is seated at a dark executive desk, both hands actively typing on a MacBook "
            "laptop keyboard. A warm brass desk lamp illuminates her face from the side. A "
            "ceramic coffee cup sits nearby. Behind her, floor-to-ceiling windows reveal a "
            "blurred city skyline at golden-hour dusk (warm bokeh lights). Shot from a 3/4 "
            "angle, waist up. Her facial expression is intensely focused and dead serious — "
            "eyes wide open, alert, brows slightly raised with sharp attention, lips pressed "
            "together firmly. No smile. She is laser-locked on the screen like a surgeon "
            "mid-operation. Powerful, precise, all-business energy. Portrait / vertical "
            "composition (roughly 3:4 aspect). Warm cinematic color grading, shallow depth "
            "of field. No text, no watermarks."
        ),
    },
    {
        "name": "donna_painpoints.png",
        "prompt": (
            "Photorealistic editorial photograph. A stylish male solo CEO / entrepreneur in his "
            "late 20s to early 30s, East-Asian descent, clean-cut with short textured dark hair, "
            "light stubble, sharp jawline. He wears a fitted black turtleneck or minimalist dark "
            "crew-neck sweater — Steve Jobs meets modern startup founder vibe. He is sitting in a "
            "sleek modern office with dark walls, designer furniture, and ambient mood lighting. "
            "Two ultrawide monitors in front of him are covered in dozens of browser tabs and "
            "notification pop-ups. Sticky notes and papers are scattered across an otherwise "
            "clean dark desk. His phone is buzzing. He presses both hands against his temples, "
            "brow furrowed, eyes closed — exhausted and overwhelmed despite the cool surroundings. "
            "The contrast is the point: great office, drowning in chaos. This is the 'before "
            "SoDonna' moment. Wide cinematic format (roughly 12:5 aspect). Moody, slightly "
            "desaturated color grading. No text, no watermarks."
        ),
    },
    {
        "name": "donna_philosophy.png",
        "prompt": (
            "Photorealistic editorial photograph. The same stylish male solo CEO / entrepreneur "
            "in his late 20s to early 30s, East-Asian descent, clean-cut with short textured dark "
            "hair, light stubble, sharp jawline. He wears a fitted black turtleneck or minimalist "
            "dark crew-neck sweater. He is leaning back comfortably in a high-back leather office "
            "chair in his sleek modern office with dark walls and designer furniture. A MacBook is "
            "open on the desk but his gaze drifts toward the floor-to-ceiling window, a calm "
            "satisfied smile on his lips. Golden afternoon sunlight pours through the glass, "
            "bathing the scene in warm light. His posture is open and relaxed — everything is "
            "under control now. One hand rests on the armrest. The mood is quiet confidence: "
            "Donna is handling everything. Wide cinematic format (roughly 2:1 aspect). "
            "Warm golden color grading. No text, no watermarks."
        ),
    },
    {
        "name": "donna_footer.png",
        "prompt": (
            f"Photorealistic editorial close-up portrait. {DONNA_ANCHOR} "
            "Cropped from the shoulders up. She looks directly into the camera with a knowing "
            "half-smile — the expression of someone who already has every answer. Warm brass "
            "desk-lamp light falls on her face from the left, creating soft Rembrandt-style "
            "shadows on the opposite cheek. Dark office background, heavily blurred. Shallow "
            "depth of field. Intimate, powerful, and warm. Suitable for circular avatar crop. "
            "Square composition (1:1 aspect). Warm cinematic color grading. No text, no watermarks."
        ),
    },
    # --- Feature UI mockups (3, unchanged) ---
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
