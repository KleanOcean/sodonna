"""Generate Raymond Yoach profile, tennis, lifestyle images + updated team photo."""

import json
from pathlib import Path
from google import genai
from google.genai import types

config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
api_key = config["providers"]["gemini"]["apiKey"]
client = genai.Client(api_key=api_key)

out_dir = Path("/Users/mac/Documents/git_repo/YoachProject/TENO-Hub/teams/assets")

RAYMOND_HAIR = "messy tousled black hair, longer and wild on top with strands going in different directions, untamed Einstein-like hairstyle"
RAYMOND_GLASSES = "rectangular thin black-frame glasses"
RAYMOND = (
    f"a man with {RAYMOND_HAIR}, wearing {RAYMOND_GLASSES}. "
    f"Hong Kong Chinese, age 30, light skin, sharp intelligent dark brown eyes behind {RAYMOND_GLASSES}, clean-shaven, defined eyebrows, "
    f"straight nose, confident calm smile, angular face with high cheekbones, lean tall build, "
    f"unconventional genius appearance like a young tech visionary, scholarly yet eccentric, quiet intensity. "
    f"IMPORTANT: he has {RAYMOND_HAIR} and always wears {RAYMOND_GLASSES}"
)

STYLE = "Square 1:1 aspect ratio. Modern flat vector illustration, clean lines, minimal detail, consistent art style throughout."

images = [
    ("raymond_profile", f"Portrait headshot of {RAYMOND}, wearing a crisp white dress shirt with top button open, no tie. Soft deep navy blue background. {STYLE}"),
    ("raymond_tennis", f"{RAYMOND} wearing a white tennis polo and white shorts, hitting an elegant forehand on a hard court under stadium lights at night, composed athletic form, confident expression. {STYLE}"),
    ("raymond_lifestyle", f"{RAYMOND} wearing a white dress shirt with sleeves rolled up, standing in front of a large glass whiteboard covered with mathematical equations and robot schematics, in a modern open-plan office, holding a marker, deep in thought. {STYLE}"),
]

for filename, prompt in images:
    print(f"Generating {filename}...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                path = out_dir / f"{filename}.png"
                path.write_bytes(part.inline_data.data)
                print(f"  Saved: {path} ({len(part.inline_data.data)} bytes)")
                break
        else:
            print(f"  WARNING: No image generated for {filename}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone!")
