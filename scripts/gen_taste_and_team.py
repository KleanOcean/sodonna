"""Generate 8 taste/品味 scene images + 1 Dawnflow uniform team photo."""

import json
from pathlib import Path
from google import genai
from google.genai import types

config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
api_key = config["providers"]["gemini"]["apiKey"]
client = genai.Client(api_key=api_key)

out_dir = Path("/Users/mac/Documents/git_repo/YoachProject/TENO-Hub/teams/assets")
out_dir.mkdir(parents=True, exist_ok=True)

STYLE = "Square 1:1 aspect ratio. Modern flat vector illustration, clean lines, minimal detail, consistent art style throughout."

# === Locked character descriptions ===

RAYMOND_HAIR = "messy tousled black hair, longer and wild on top with strands going in different directions, untamed Einstein-like hairstyle"
RAYMOND_GLASSES = "rectangular thin black-frame glasses"
RAYMOND = (
    f"a man with {RAYMOND_HAIR}, wearing {RAYMOND_GLASSES}. "
    f"Hong Kong Chinese, age 30, light skin, sharp intelligent dark brown eyes behind {RAYMOND_GLASSES}, clean-shaven, defined eyebrows, "
    f"straight nose, confident calm smile, angular face with high cheekbones, lean tall build, "
    f"unconventional genius appearance like a young tech visionary, scholarly yet eccentric, quiet intensity. "
    f"IMPORTANT: he has {RAYMOND_HAIR} and always wears {RAYMOND_GLASSES}"
)

ELENA = (
    "a woman: Italian-American, age 35, shoulder-length brown bob hair with a slight wave parted on the left, "
    "warm olive skin tone, dark brown almond-shaped eyes, thin arched eyebrows, small straight nose, "
    "full lips with a warm smile, oval face shape, slender build"
)

MARCO = (
    "a man: Chinese, age 32, very short cropped black hair with a subtle fade on the sides, "
    "light tan skin, small dark brown eyes, thick straight eyebrows, broad flat nose, "
    "wide friendly smile showing teeth, square jawline, strong stocky athletic build"
)

ETHAN = (
    "a man: Chinese, age 29, neat short black hair parted on the right, "
    "pale skin, dark brown eyes behind round thin-frame black glasses, thin eyebrows, "
    "small pointed nose, closed-mouth subtle smile, narrow oval face, slim build"
)

KEVIN = (
    "a man: Chinese, age 31, short buzzcut black hair, "
    "medium tan skin, small sharp dark brown eyes, straight thick eyebrows, "
    "medium nose, neutral focused expression with slight smile, angular face with defined cheekbones, lean build"
)

MARCUS = (
    "a man: German Caucasian, age 29, light brown hair neatly side-parted to the left, "
    "fair pinkish skin, blue-grey eyes, light brown thin eyebrows, straight narrow nose, "
    "serious composed expression, rectangular face with strong chin, tall athletic build"
)

QUINN = (
    "a man: Chinese, age 32, styled black hair swept back with volume on top, "
    "light skin, dark brown eyes, groomed thin eyebrows, straight nose, "
    "polished confident smile, oval face, medium build, fashionable appearance"
)

LUCAS = (
    "a man: Brazilian mixed-race, age 32, dark brown curly hair medium length, "
    "warm medium-brown skin, brown eyes, thick dark eyebrows, slightly wide nose, "
    "big warm open smile showing teeth, round friendly face, medium athletic build"
)

UNIFORM = "wearing a matching plain black crew-neck t-shirt with a small white geometric logo on the left chest (a rounded triangle with a circle inside it, and the word Dawnflow next to it in white)"

images = [
    # ===== TEAM PHOTO (Dawnflow uniforms) =====
    ("team_photo", (
        f"A group photo of 8 tech professionals standing together on an outdoor tennis court, "
        f"sunny day, tennis net behind them. ALL wearing identical matching plain black crew-neck t-shirts with a small white logo on the left chest. Left to right: "
        f"1) {ELENA} {UNIFORM}; "
        f"2) {MARCO} {UNIFORM}; "
        f"3) {ETHAN} {UNIFORM}; "
        f"4) {RAYMOND} {UNIFORM}, standing in the center as the leader; "
        f"5) {KEVIN} {UNIFORM}; "
        f"6) {MARCUS} {UNIFORM}; "
        f"7) {QUINN} {UNIFORM}; "
        f"8) {LUCAS} {UNIFORM}. "
        f"They are standing shoulder to shoulder, relaxed and confident, some holding tennis rackets. "
        f"Modern flat vector illustration, clean lines, vibrant colors, 16:9 wide aspect ratio."
    )),

    # ===== TASTE/品味 SCENES =====
    ("raymond_taste", f"{RAYMOND} sitting alone in a quiet university corridor at night, leaning against the wall next to a closed office door, a notebook open on his lap, holding a sleek black fountain pen, warm dim hallway lighting, contemplative peaceful expression. {STYLE}"),

    ("T1_elena_taste", f"{ELENA} sitting at a small Italian restaurant table by the seaside at sunset, a Negroni cocktail on the table, reading a Japanese book, warm golden light, an Alfa Romeo visible parked outside through the window, elegant relaxed evening mood. {STYLE}"),

    ("T2_marco_taste", f"{MARCO} crouching on a factory floor in a CNC machining workshop, holding digital calipers measuring a metal part, wearing a dark polo and safety glasses pushed up on his forehead, industrial lighting, shelves of metal parts in background, focused craftsman expression. {STYLE}"),

    ("T3_ethan_taste", f"{ETHAN} sitting alone in a minimalist art museum gallery, natural light streaming from above, a large impressionist painting on the white wall, holding a camera, contemplative peaceful expression, clean architectural space. {STYLE}"),

    ("T4_kevin_taste", f"{KEVIN} in a university electronics lab late at night, an oscilloscope showing green waveforms on screen, a small circuit board on the workbench, soldering iron nearby, dim warm desk lamp, focused satisfied expression. {STYLE}"),

    ("T5_marcus_taste", f"{MARCUS} at a clean minimal desk, a black ThinkPad laptop open showing code, a red pen in hand writing in a hardcover notebook, a minimalist round watch on his wrist, a plain black coffee cup, morning light from window, precise organized workspace. {STYLE}"),

    ("T6_quinn_taste", f"{QUINN} riding a black folding bicycle along a lakeside path at dusk, West Lake scenery with willows and pagoda silhouette in background, wearing a casual white t-shirt and jeans, earbuds in, relaxed happy expression, warm golden hour light. {STYLE}"),

    ("T7_lucas_taste", f"{LUCAS} at a lively outdoor street bar in São Paulo, holding a Caipirinha cocktail, string lights above, colorful buildings in background, laughing with friends, warm tropical evening atmosphere, festive relaxed mood. {STYLE}"),
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
        print(f"  ERROR generating {filename}: {e}")

print("\nDone! Generated 9 images.")
