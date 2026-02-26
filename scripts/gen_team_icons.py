"""Generate all team images with consistent facial features per person + group photo."""

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

# === Locked character descriptions (used identically in all 3 images) ===

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

images = [
    # ===== TEAM PHOTO =====
    ("team_photo", (
        f"A group photo of 8 tech professionals standing together on an outdoor tennis court, "
        f"sunny day, tennis net behind them. Left to right: "
        f"1) {ELENA} wearing a black turtleneck; "
        f"2) {MARCO} wearing a dark navy polo; "
        f"3) {ETHAN} wearing a grey crew neck sweater; "
        f"4) {RAYMOND} wearing a crisp white dress shirt with top button open, standing in the center as the leader; "
        f"5) {KEVIN} wearing a white t-shirt; "
        f"6) {MARCUS} wearing a navy button-down shirt; "
        f"7) {QUINN} wearing a dark casual blazer over black crew neck; "
        f"8) {LUCAS} wearing an olive green henley shirt. "
        f"They are standing shoulder to shoulder, relaxed and confident, some holding tennis rackets. "
        f"Modern flat vector illustration, clean lines, vibrant colors, 16:9 wide aspect ratio."
    )),

    # ===== T1 Elena Rossi =====
    ("T1_elena", f"Portrait headshot of {ELENA}, wearing a black turtleneck. Soft coral pink background. {STYLE}"),
    ("T1_elena_tennis", f"{ELENA} wearing a black tennis dress and black visor cap, hitting a one-handed backhand on a red clay tennis court, warm sunset lighting, trees in background. {STYLE}"),
    ("T1_elena_lifestyle", f"{ELENA} wearing a teal blouse, sitting in a minimalist co-working space with floor-to-ceiling windows showing a city skyline, sketching wireframes on an iPad with Apple Pencil, espresso cup on the desk. {STYLE}"),

    # ===== T2 Marco Zhao =====
    ("T2_marco", f"Portrait headshot of {MARCO}, wearing a dark navy polo shirt. Soft blue-grey background. {STYLE}"),
    ("T2_marco_tennis", f"{MARCO} wearing a dark blue tennis polo and white shorts, hitting a powerful flat serve tossing the ball high on a hard court, bright daylight. {STYLE}"),
    ("T2_marco_lifestyle", f"{MARCO} wearing a dark blue polo, inspecting a drone prototype in a factory workshop, tools and mechanical parts on workbench, industrial lighting. {STYLE}"),

    # ===== T3 Ethan Chen =====
    ("T3_ethan", f"Portrait headshot of {ETHAN}, wearing a grey crew neck sweater. Soft mint green background. {STYLE}"),
    ("T3_ethan_tennis", f"{ETHAN} wearing a grey tennis shirt, sitting courtside analyzing shot data on a tablet, tennis racket leaning beside him, analytical focused expression. {STYLE}"),
    ("T3_ethan_lifestyle", f"{ETHAN} wearing a grey sweater, working late at night in a lab with multiple monitors showing colorful data visualizations and point clouds, coffee mug on desk. {STYLE}"),

    # ===== T4 Kevin Huang =====
    ("T4_kevin", f"Portrait headshot of {KEVIN}, wearing a plain white t-shirt. Soft warm yellow background. {STYLE}"),
    ("T4_kevin_tennis", f"{KEVIN} wearing a white tennis shirt, examining a tennis racket string pattern closely with curiosity on a practice court, casual weekend vibe. {STYLE}"),
    ("T4_kevin_lifestyle", f"{KEVIN} wearing a white t-shirt, soldering at a workbench with oscilloscope showing waveforms, circuit boards and electronic components on desk, focused expression. {STYLE}"),

    # ===== T5 Marcus Weber =====
    ("T5_marcus", f"Portrait headshot of {MARCUS}, wearing a navy button-down shirt. Soft steel blue background. {STYLE}"),
    ("T5_marcus_tennis", f"{MARCUS} wearing a navy tennis polo and white shorts, rushing to the net for a volley on an indoor court, disciplined athletic form. {STYLE}"),
    ("T5_marcus_lifestyle", f"{MARCUS} wearing a navy button-down shirt, standing in front of a whiteboard covered with system architecture diagrams and flowcharts in an office, presenting. {STYLE}"),

    # ===== T6 Quinn Xu =====
    ("T6_quinn", f"Portrait headshot of {QUINN}, wearing a dark casual blazer over black crew neck. Soft lavender purple background. {STYLE}"),
    ("T6_quinn_tennis", f"{QUINN} wearing a dark tennis jacket, playing doubles on a tennis court, high-fiving his partner after a point, energetic happy expression. {STYLE}"),
    ("T6_quinn_lifestyle", f"{QUINN} wearing a casual blazer, sitting in a lakeside cafe with a laptop showing colorful code on screen, AirPods in ears, relaxed creative vibe, greenery outside. {STYLE}"),

    # ===== T7 Lucas Fernandez =====
    ("T7_lucas", f"Portrait headshot of {LUCAS}, wearing an olive green henley shirt. Soft warm peach orange background. {STYLE}"),
    ("T7_lucas_tennis", f"{LUCAS} wearing an olive green tennis shirt and white shorts, in a defensive low sliding position returning a deep shot on a blue hard court, determined expression. {STYLE}"),
    ("T7_lucas_lifestyle", f"{LUCAS} wearing an olive henley, sitting at a rooftop bar with city skyline at dusk behind him, laptop showing colorful test dashboards, warm friendly smile. {STYLE}"),
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

print("\nDone!")
