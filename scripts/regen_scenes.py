"""Regenerate all 24 scene images with hair-consistent prompts."""

import json, time
from pathlib import Path
from google import genai
from google.genai import types

config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
api_key = config["providers"]["gemini"]["apiKey"]
client = genai.Client(api_key=api_key)

out_dir = Path("/Users/mac/Documents/git_repo/YoachProject/TENO-Hub/teams/assets")

STYLE = "Square 1:1 aspect ratio. Modern flat vector illustration, clean lines, minimal detail, consistent art style throughout."

# === Hair-first character descriptions ===
# Hair is placed FIRST and repeated for emphasis

RAYMOND_HAIR = "medium-length neat black hair slightly longer on top swept to the right"
RAYMOND = (
    f"a man with {RAYMOND_HAIR}. "
    f"Hong Kong Chinese, age 30, light skin, sharp intelligent dark brown eyes, clean-shaven, defined eyebrows, "
    f"straight nose, confident calm smile, angular face with high cheekbones, lean tall build, "
    f"handsome and scholarly appearance with a quiet intensity. "
    f"IMPORTANT: his hair is {RAYMOND_HAIR}"
)

ELENA_HAIR = "shoulder-length brown bob hair with a slight wave parted on the left, ending just above the shoulders"
ELENA = (
    f"a woman with {ELENA_HAIR}. "
    f"Italian-American, age 35, warm olive skin tone, dark brown almond-shaped eyes, thin arched eyebrows, "
    f"small straight nose, full lips with a warm smile, oval face shape, slender build. "
    f"IMPORTANT: her hair is a {ELENA_HAIR}"
)

MARCO_HAIR = "very short cropped black hair with a subtle fade on the sides, almost buzzcut-short"
MARCO = (
    f"a man with {MARCO_HAIR}. "
    f"Chinese, age 32, light tan skin, small dark brown eyes, thick straight eyebrows, broad flat nose, "
    f"wide friendly smile showing teeth, square jawline, strong stocky athletic build. "
    f"IMPORTANT: his hair is {MARCO_HAIR}"
)

ETHAN_HAIR = "neat short black hair parted on the right, flat and tidy"
ETHAN = (
    f"a man with {ETHAN_HAIR}. "
    f"Chinese, age 29, pale skin, dark brown eyes behind round thin-frame black glasses, thin eyebrows, "
    f"small pointed nose, closed-mouth subtle smile, narrow oval face, slim build. "
    f"IMPORTANT: his hair is {ETHAN_HAIR}, and he always wears round thin-frame black glasses"
)

KEVIN_HAIR = "short buzzcut black hair, very short and even all around"
KEVIN = (
    f"a man with {KEVIN_HAIR}. "
    f"Chinese, age 31, medium tan skin, small sharp dark brown eyes, straight thick eyebrows, "
    f"medium nose, neutral focused expression with slight smile, angular face with defined cheekbones, lean build. "
    f"IMPORTANT: his hair is {KEVIN_HAIR}"
)

MARCUS_HAIR = "light brown hair neatly side-parted to the left, short and tidy"
MARCUS = (
    f"a man with {MARCUS_HAIR}. "
    f"German Caucasian, age 29, fair pinkish skin, blue-grey eyes, light brown thin eyebrows, straight narrow nose, "
    f"serious composed expression, rectangular face with strong chin, tall athletic build. "
    f"IMPORTANT: his hair is {MARCUS_HAIR}"
)

QUINN_HAIR = "styled black hair swept back with volume on top"
QUINN = (
    f"a man with {QUINN_HAIR}. "
    f"Chinese, age 32, light skin, dark brown eyes, groomed thin eyebrows, straight nose, "
    f"polished confident smile, oval face, medium build, fashionable appearance. "
    f"IMPORTANT: his hair is {QUINN_HAIR}"
)

LUCAS_HAIR = "dark brown curly hair medium length"
LUCAS = (
    f"a man with {LUCAS_HAIR}. "
    f"Brazilian mixed-race, age 32, warm medium-brown skin, brown eyes, thick dark eyebrows, slightly wide nose, "
    f"big warm open smile showing teeth, round friendly face, medium athletic build. "
    f"IMPORTANT: his hair is {LUCAS_HAIR}"
)

images = [
    # === Raymond (3 scenes) ===
    ("raymond_tennis", f"{RAYMOND} wearing a white tennis polo and white shorts, hitting an elegant forehand on a hard court under stadium lights at night, composed athletic form, confident expression. {STYLE}"),
    ("raymond_lifestyle", f"{RAYMOND} wearing a white dress shirt with sleeves rolled up, standing in front of a large glass whiteboard covered with mathematical equations and robot schematics, in a modern open-plan office, holding a marker, deep in thought. {STYLE}"),
    ("raymond_taste", f"{RAYMOND} sitting alone in a quiet university corridor at night, leaning against the wall next to a closed office door, a notebook open on his lap, holding a sleek black fountain pen, warm dim hallway lighting, contemplative peaceful expression. {STYLE}"),

    # === T1 Elena (3 scenes) ===
    ("T1_elena_tennis", f"{ELENA} wearing a black tennis dress and black visor cap, hitting a one-handed backhand on a red clay tennis court, warm sunset lighting, trees in background. {STYLE}"),
    ("T1_elena_lifestyle", f"{ELENA} wearing a teal blouse, sitting in a minimalist co-working space with floor-to-ceiling windows showing a city skyline, sketching wireframes on an iPad with Apple Pencil, espresso cup on the desk. {STYLE}"),
    ("T1_elena_taste", f"{ELENA} sitting at a small Italian restaurant table by the seaside at sunset, a Negroni cocktail on the table, reading a Japanese book, warm golden light, an Alfa Romeo visible parked outside through the window, elegant relaxed evening mood. {STYLE}"),

    # === T2 Marco (3 scenes) ===
    ("T2_marco_tennis", f"{MARCO} wearing a dark blue tennis polo and white shorts, hitting a powerful flat serve tossing the ball high on a hard court, bright daylight. {STYLE}"),
    ("T2_marco_lifestyle", f"{MARCO} wearing a dark blue polo, inspecting a drone prototype in a factory workshop, tools and mechanical parts on workbench, industrial lighting. {STYLE}"),
    ("T2_marco_taste", f"{MARCO} crouching on a factory floor in a CNC machining workshop, holding digital calipers measuring a metal part, wearing a dark polo and safety glasses pushed up on his forehead, industrial lighting, shelves of metal parts in background, focused craftsman expression. {STYLE}"),

    # === T3 Ethan (3 scenes) ===
    ("T3_ethan_tennis", f"{ETHAN} wearing a grey tennis shirt, sitting courtside analyzing shot data on a tablet, tennis racket leaning beside him, analytical focused expression. {STYLE}"),
    ("T3_ethan_lifestyle", f"{ETHAN} wearing a grey sweater, working late at night in a lab with multiple monitors showing colorful data visualizations and point clouds, coffee mug on desk. {STYLE}"),
    ("T3_ethan_taste", f"{ETHAN} sitting alone in a minimalist art museum gallery, natural light streaming from above, a large impressionist painting on the white wall, holding a camera, contemplative peaceful expression, clean architectural space. {STYLE}"),

    # === T4 Kevin (3 scenes) ===
    ("T4_kevin_tennis", f"{KEVIN} wearing a white tennis shirt, examining a tennis racket string pattern closely with curiosity on a practice court, casual weekend vibe. {STYLE}"),
    ("T4_kevin_lifestyle", f"{KEVIN} wearing a white t-shirt, soldering at a workbench with oscilloscope showing waveforms, circuit boards and electronic components on desk, focused expression. {STYLE}"),
    ("T4_kevin_taste", f"{KEVIN} in a university electronics lab late at night, an oscilloscope showing green waveforms on screen, a small circuit board on the workbench, soldering iron nearby, dim warm desk lamp, focused satisfied expression. {STYLE}"),

    # === T5 Marcus (3 scenes) ===
    ("T5_marcus_tennis", f"{MARCUS} wearing a navy tennis polo and white shorts, rushing to the net for a volley on an indoor court, disciplined athletic form. {STYLE}"),
    ("T5_marcus_lifestyle", f"{MARCUS} wearing a navy button-down shirt, standing in front of a whiteboard covered with system architecture diagrams and flowcharts in an office, presenting. {STYLE}"),
    ("T5_marcus_taste", f"{MARCUS} at a clean minimal desk, a black ThinkPad laptop open showing code, a red pen in hand writing in a hardcover notebook, a minimalist round watch on his wrist, a plain black coffee cup, morning light from window, precise organized workspace. {STYLE}"),

    # === T6 Quinn (3 scenes) ===
    ("T6_quinn_tennis", f"{QUINN} wearing a dark tennis jacket, playing doubles on a tennis court, high-fiving his partner after a point, energetic happy expression. {STYLE}"),
    ("T6_quinn_lifestyle", f"{QUINN} wearing a casual blazer, sitting in a lakeside cafe with a laptop showing colorful code on screen, AirPods in ears, relaxed creative vibe, greenery outside. {STYLE}"),
    ("T6_quinn_taste", f"{QUINN} riding a black folding bicycle along a lakeside path at dusk, West Lake scenery with willows and pagoda silhouette in background, wearing a casual white t-shirt and jeans, earbuds in, relaxed happy expression, warm golden hour light. {STYLE}"),

    # === T7 Lucas (3 scenes) ===
    ("T7_lucas_tennis", f"{LUCAS} wearing an olive green tennis shirt and white shorts, in a defensive low sliding position returning a deep shot on a blue hard court, determined expression. {STYLE}"),
    ("T7_lucas_lifestyle", f"{LUCAS} wearing an olive henley, sitting at a rooftop bar with city skyline at dusk behind him, laptop showing colorful test dashboards, warm friendly smile. {STYLE}"),
    ("T7_lucas_taste", f"{LUCAS} at a lively outdoor street bar in São Paulo, holding a Caipirinha cocktail, string lights above, colorful buildings in background, laughing with friends, warm tropical evening atmosphere, festive relaxed mood. {STYLE}"),
]

print(f"Regenerating {len(images)} scene images with hair-consistent prompts...\n")

for i, (filename, prompt) in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {filename}...")
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
    # small delay to avoid rate limiting
    if i < len(images) - 1:
        time.sleep(1)

print(f"\nDone! Regenerated {len(images)} scene images.")
