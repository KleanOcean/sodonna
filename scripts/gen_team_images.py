"""Batch generate team images using Gemini image generation.

Two-pass approach for visual consistency:
  Pass 1: Generate profile photos for each person
  Pass 2: Use each profile as reference image to generate 3 variants
  Pass 3: Generate team photo using all 8 profiles as reference

Usage:
    python3 gen_team_images.py              # generate all images
    python3 gen_team_images.py --dry-run    # print prompts without generating
    python3 gen_team_images.py --only klean # generate only klean's images
    python3 gen_team_images.py --pass2-only # skip profile generation, regenerate variants only
"""

import json
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO = Path(__file__).parent
ASSETS_DIR = REPO / "assets" / "images"
TEAM_DIR = ASSETS_DIR / "team"

config = json.loads((Path.home() / ".nanobot" / "config.json").read_text())
API_KEY = config["providers"]["gemini"]["apiKey"]

# ---------------------------------------------------------------------------
# Physical identity anchors — the SAME description used in every prompt
# for that person so Gemini generates consistent faces.
# ---------------------------------------------------------------------------
IDENTITY = {
    "klean": (
        "a 30-year-old Hong Kong Chinese man with a clean side-parted short black hair, "
        "defined jawline, slim athletic build (175 cm), subtle confident smile, "
        "dark brown eyes, light stubble, straight nose bridge. "
    ),
    "t1_elena": (
        "a 35-year-old Italian-American woman with shoulder-length auburn/chestnut hair, "
        "olive-toned skin, hazel-green eyes, high cheekbones, elegant bone structure, "
        "medium build (170 cm), warm Mediterranean features. "
    ),
    "t2_marco": (
        "a 32-year-old Chinese man with short neat black hair (crew cut on sides, "
        "slightly longer on top), broad shoulders, strong athletic build (180 cm), "
        "square jawline, thick eyebrows, dark brown eyes, tanned skin from outdoor work. "
    ),
    "t3_kavya": (
        "a 29-year-old Indian woman with long dark brown hair usually in a loose side braid, "
        "warm brown skin, dark expressive eyes, oval face with high cheekbones, "
        "slim build (165 cm), confident and calm expression, small nose stud on left nostril. "
    ),
    "t4_kevin": (
        "a 31-year-old Chinese man with slightly tousled medium-length black hair, "
        "average build (176 cm), round face with soft features, small eyes with "
        "single eyelids, friendly approachable expression, clean-shaven. "
    ),
    "t5_marcus": (
        "a 29-year-old German man with light brown/sandy hair neatly combed to the side, "
        "tall lean build (188 cm), sharp blue eyes, angular Germanic features, "
        "high forehead, thin lips, clean-shaven, precise composed expression. "
    ),
    "t6_soyeon": (
        "a 31-year-old Korean woman with shoulder-length straight black hair with subtle "
        "layers, fair porcelain skin, almond-shaped dark brown eyes, small face with soft "
        "jawline, slim build (167 cm), minimal natural makeup, elegant and stylish. "
    ),
    "t7_lucas": (
        "a 32-year-old Brazilian man with curly dark brown hair (medium length, natural curls), "
        "warm brown skin, broad warm smile showing white teeth, brown eyes, "
        "medium-athletic build (178 cm), slight stubble, friendly expressive face. "
    ),
}

# ---------------------------------------------------------------------------
# Person definitions: profile prompt + 3 variant scene prompts
# ---------------------------------------------------------------------------
PEOPLE = {
    "klean": {
        "profile_path": TEAM_DIR / "klean_profile.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred modern office with a whiteboard. "
            "Natural window light from the left, slight rim light. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field, eye-level. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "klean_tennis.png",
                "Photorealistic action photo of {identity}"
                "He is playing tennis at night under bright floodlights, mid-forehand swing, "
                "powerful and precise form. Wearing a black athletic t-shirt. "
                "Hard court surface. Ball visible mid-flight. Slight motion blur on racket. "
                "Shot on Sony A7IV 70-200mm f/2.8."
            ),
            (
                TEAM_DIR / "klean_lifestyle.png",
                "Photorealistic photo of {identity}"
                "He is standing at a large whiteboard in a modern Hong Kong office, writing "
                "mathematical topology equations with a blue marker. Wearing a black crew-neck "
                "t-shirt with 'Dawnflow' logo. Focused contemplative expression, side profile view. "
                "Floor-to-ceiling windows showing Hong Kong cityscape. A Lamy 2000 fountain pen "
                "on the desk. Natural daylight. Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "klean_taste.png",
                "Photorealistic photo of {identity}"
                "He is sitting alone on the floor in a modern university corridor at golden hour. "
                "Concrete and glass architecture (HKUST style). Leaning against the wall, "
                "pensive expression, looking at sunset light through large windows. "
                "Wearing a black t-shirt, khaki pants. A notebook open on his lap, a pen in hand. "
                "Quiet, reflective, solitary mood. Shot on Sony A7IV 35mm f/1.4."
            ),
        ],
    },
    "t1_elena": {
        "profile_path": TEAM_DIR / "t1_elena.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred modern tech office. "
            "Warm natural window light. Confident, creative expression. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t1_elena_tennis.png",
                "Photorealistic action photo of {identity}"
                "She is playing tennis on a European red clay court, hitting a beautiful "
                "one-handed backhand. Auburn hair in a ponytail. Wearing a white tennis dress. "
                "Red clay dust rising from her shoes. Cypress trees in the background. "
                "Shot on Sony A7IV 70-200mm."
            ),
            (
                TEAM_DIR / "t1_elena_lifestyle.png",
                "Photorealistic photo of {identity}"
                "She is sitting at a modern standing desk in a bright Shenzhen office, sketching "
                "product wireframes on an iPad Pro with Apple Pencil. Wearing a relaxed COS linen "
                "shirt in beige. A Cartier Tank Française watch visible on her wrist. Clean minimal "
                "workspace, large monitor showing UI mockups. Natural lighting from windows. "
                "Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t1_elena_taste.png",
                "Photorealistic photo of {identity}"
                "She is sitting at a small Italian restaurant bar in Shekou, Shenzhen at twilight. "
                "Holding a Negroni cocktail (orange-red drink with orange peel). Warm amber "
                "ambient lighting. Mediterranean ceramic tile decor. Through an arched window, "
                "a harbor with boats. A Japanese design book open on the bar counter. "
                "Relaxed elegant mood. Shot on Sony A7IV 50mm."
            ),
        ],
    },
    "t2_marco": {
        "profile_path": TEAM_DIR / "t2_marco.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred hardware lab. "
            "Confident, hands-on engineer look. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t2_marco_tennis.png",
                "Photorealistic action photo of {identity}"
                "He is serving a tennis ball with great power — full trophy pose, arm extended high. "
                "Wearing a black athletic t-shirt. Outdoor hard court. Dynamic low angle shot "
                "looking up at the serve. Bright daytime. Shot on Sony A7IV 70-200mm f/2.8."
            ),
            (
                TEAM_DIR / "t2_marco_lifestyle.png",
                "Photorealistic photo of {identity}"
                "He is crouching on a Dongguan CNC factory floor, inspecting an aluminum robot "
                "chassis part with a Mitutoyo digital caliper. Wearing a black polo shirt, "
                "safety glasses pushed up on his forehead. Industrial CNC machines and metal "
                "shavings in background. Fluorescent factory lighting. "
                "Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t2_marco_taste.png",
                "Photorealistic close-up photo of {identity}"
                "He is sitting at a workshop workbench, hands carefully measuring an aluminum "
                "CNC part with digital calipers. On the table: a Moleskine grid notebook with "
                "hand-drawn mechanical sketches, a Pentel GraphGear 1000 pencil, metal shavings. "
                "Focused craftsman expression. Warm workshop lamp lighting. "
                "Shot on Sony A7IV 50mm macro."
            ),
        ],
    },
    "t3_kavya": {
        "profile_path": TEAM_DIR / "t3_kavya.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred robotics lab with monitors. "
            "Confident, calm, analytical expression. Small nose stud visible on left nostril. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t3_kavya_tennis.png",
                "Photorealistic action photo of {identity}"
                "She is hitting a powerful baseline forehand on an outdoor hard court, "
                "athletic stance, weight transferred forward. Long dark hair in a ponytail. "
                "Wearing black athletic t-shirt. Daytime, bright sunshine. "
                "Determined focused expression. Shot on Sony A7IV 70-200mm f/2.8."
            ),
            (
                TEAM_DIR / "t3_kavya_lifestyle.png",
                "Photorealistic photo of {identity}"
                "She is working late at night in a Shanghai robotics lab. Multiple monitors "
                "showing colorful LiDAR point cloud data and ROS2 rviz visualizations. "
                "Wearing a black t-shirt, hair in a loose side braid. A small wheeled robot "
                "prototype on the bench nearby. Blue screen glow illuminating her face. "
                "Deep focus, night-owl engineer mood. Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t3_kavya_taste.png",
                "Photorealistic photo of {identity}"
                "She is walking barefoot on Juhu Beach in Mumbai at sunset, "
                "Arabian Sea waves lapping at her feet. Wearing a casual kurta top and jeans, "
                "hair loose in the ocean breeze. Golden-orange sunset sky. "
                "Looking at the horizon with a peaceful, reflective expression. "
                "Warm golden hour light. Shot on Sony A7IV 35mm f/1.4."
            ),
        ],
    },
    "t4_kevin": {
        "profile_path": TEAM_DIR / "t4_kevin.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred electronics workbench. "
            "Friendly, curious engineer expression. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t4_kevin_tennis.png",
                "Photorealistic photo of {identity}"
                "He is on a tennis court, holding his racket up to the sunlight and closely "
                "examining the string tension pattern with an engineer's curiosity, squinting. "
                "Wearing black athletic shirt. Casual weekend player vibe. Outdoor court, "
                "afternoon light. Shot on Sony A7IV 85mm."
            ),
            (
                TEAM_DIR / "t4_kevin_lifestyle.png",
                "Photorealistic photo of {identity}"
                "He is in a Shenzhen makerspace, soldering an ESP32 development board under "
                "a magnifying lamp. Wearing a black t-shirt. On the desk: an oscilloscope "
                "showing PWM waveforms, a white HHKB Professional Classic keyboard, "
                "Sennheiser HD 600 headphones around his neck, a half-finished pour-over coffee. "
                "Warm desk lamp lighting against a dark background. Shot on Sony A7IV 50mm."
            ),
            (
                TEAM_DIR / "t4_kevin_taste.png",
                "Photorealistic photo of {identity}"
                "He is in a dimly lit university electronics lab at 3 AM, smiling in triumph "
                "while looking at an oscilloscope displaying a perfect stable PWM waveform. "
                "An STM32 development board with three small servo motors sits on the workbench. "
                "Two colleagues celebrate beside him. ETH Zurich-style basement lab. "
                "Warm fluorescent lighting. Camaraderie mood. Shot on Sony A7IV 35mm."
            ),
        ],
    },
    "t5_marcus": {
        "profile_path": TEAM_DIR / "t5_marcus.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred minimalist office. "
            "Precise, composed expression with a hint of German engineering discipline. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t5_marcus_tennis.png",
                "Photorealistic action photo of {identity}"
                "He is at the tennis net executing a crisp forehand volley, athletic forward "
                "lunge. Tall lean build. Wearing black athletic shirt. Hard court. "
                "Quick reflexive movement captured mid-action. "
                "Shot on Sony A7IV 70-200mm f/2.8."
            ),
            (
                TEAM_DIR / "t5_marcus_lifestyle.png",
                "Photorealistic photo of {identity}"
                "He is sitting at a minimalist Bauhaus-inspired desk in a Beijing apartment, "
                "sketching a system architecture diagram in a Leuchtturm1917 notebook with "
                "a red pen. A ThinkPad X1 Carbon with a tiling window manager (i3wm) is open "
                "beside him. A Nomos Tangente watch on his wrist. Morning sunlight from a "
                "window. Clean, disciplined workspace. Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t5_marcus_taste.png",
                "Photorealistic photo of {identity}"
                "He is sitting at the same desk early morning, reviewing code on a ThinkPad "
                "screen while making notes in a notebook with a red pen. A simple ceramic cup "
                "of black coffee (no milk). Wearing a black t-shirt. Warm morning sunlight. "
                "Disciplined ritual-like code review session. German precision aesthetic. "
                "Shot on Sony A7IV 50mm."
            ),
        ],
    },
    "t6_soyeon": {
        "profile_path": TEAM_DIR / "t6_soyeon.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred bright modern office. "
            "Warm, elegant, approachable expression. Minimal natural makeup. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t6_soyeon_tennis.png",
                "Photorealistic photo of {identity}"
                "She is on a tennis court, giving an enthusiastic high-five to her doubles "
                "partner after winning a point. Warm genuine smile. Wearing black athletic "
                "t-shirt. Outdoor hard court, bright daytime. Joyful doubles moment. "
                "Shot on Sony A7IV 85mm."
            ),
            (
                TEAM_DIR / "t6_soyeon_lifestyle.png",
                "Photorealistic photo of {identity}"
                "She is sitting at a wooden table in a stylish indie coffee shop in Shenzhen "
                "OCT-LOFT creative district. MacBook Pro open showing Figma UI design work. "
                "A flat white coffee beside the laptop. Wearing a Maison Kitsuné striped t-shirt "
                "and Acne Studios jeans. AirPods Pro on the table. Apple Watch Ultra on her wrist. "
                "Warm cafe lighting. Focused creative mood. Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t6_soyeon_taste.png",
                "Photorealistic photo of {identity}"
                "She is jogging along the Shenzhen Bay Park waterfront promenade at sunrise, "
                "wearing athletic clothes, AirPods Pro in ears. Shenzhen skyline in the "
                "background. Morning golden light reflecting on the water. Hair in a high "
                "ponytail, relaxed focused runner's expression. Energetic healthy lifestyle. "
                "Shot on Sony A7IV 70-200mm f/2.8."
            ),
        ],
    },
    "t7_lucas": {
        "profile_path": TEAM_DIR / "t7_lucas.png",
        "profile_prompt": (
            "Square 1:1 aspect ratio professional headshot of {identity}"
            "Head and shoulders framing, centered composition, like a resume or LinkedIn photo. "
            "Wearing a black crew-neck t-shirt with a small 'Dawnflow' text logo on the left chest. "
            "Background: softly blurred modern office with monitors. "
            "Warm friendly smile, approachable energy. "
            "Shot on Sony A7IV 85mm f/1.4, shallow depth of field. Square crop."
        ),
        "variants": [
            (
                TEAM_DIR / "t7_lucas_tennis.png",
                "Photorealistic action photo of {identity}"
                "He is performing a defensive sliding forehand on a hard court, low center "
                "of gravity, athletic movement. Wearing black athletic t-shirt. "
                "Determined defensive posture. Daytime outdoor court. "
                "Shot on Sony A7IV 70-200mm f/2.8."
            ),
            (
                TEAM_DIR / "t7_lucas_lifestyle.png",
                "Photorealistic photo of {identity}"
                "He is on a Shanghai rooftop terrace, working on a laptop showing test "
                "automation dashboards and green CI/CD pipeline graphs. Pudong skyline "
                "(Oriental Pearl Tower) in the background. Wearing a black t-shirt. "
                "Late afternoon golden light. A coffee cup beside the laptop. "
                "Focused but relaxed outdoor work session. Shot on Sony A7IV 35mm."
            ),
            (
                TEAM_DIR / "t7_lucas_taste.png",
                "Photorealistic photo of {identity}"
                "He is standing in a vibrant São Paulo Vila Madalena neighborhood street "
                "during Carnaval. Colorful street art murals on the walls. He holds a "
                "Caipirinha cocktail and has a broad warm smile. Wearing a casual cream "
                "linen shirt. Intimate neighborhood celebration, not the big parade. "
                "String lights above. Warm evening light. Shot on Sony A7IV 35mm."
            ),
        ],
    },
}


def generate_image(client, prompt, out_path, ref_image_bytes=None):
    """Generate a single image, optionally with a reference image for consistency."""
    rel = out_path.relative_to(REPO)

    contents = []
    if ref_image_bytes:
        # Pass the profile image as reference for visual consistency
        contents.append(
            types.Part.from_bytes(data=ref_image_bytes, mime_type="image/png")
        )
        contents.append(
            "The photo above is a reference portrait. Generate a NEW photo of "
            "this EXACT SAME person (same face, same hair, same build) in the "
            "following scene. Keep the face, hairstyle, and body type perfectly "
            "consistent with the reference:\n\n" + prompt
        )
    else:
        contents = prompt

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                out_path.write_bytes(part.inline_data.data)
                print(f"  OK: {rel} ({len(part.inline_data.data):,} bytes)")
                return True
            elif part.text is not None:
                print(f"  Text: {part.text[:120]}")

        print(f"  WARNING: No image returned for {rel}")
        return False

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv
    pass2_only = "--pass2-only" in sys.argv
    only = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        only = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

    TEAM_DIR.mkdir(parents=True, exist_ok=True)

    # Filter people
    people = {k: v for k, v in PEOPLE.items() if not only or only in k}
    total = sum(1 + len(v["variants"]) for v in people.values()) + (0 if only else 1)
    print(f"\n{'[DRY RUN] ' if dry_run else ''}{len(people)} people, ~{total} images\n")

    if dry_run:
        for key, person in people.items():
            identity = IDENTITY[key]
            print(f"=== {key} PROFILE ===")
            print(person["profile_prompt"].format(identity=identity)[:200] + "...\n")
            for path, prompt in person["variants"]:
                rel = path.relative_to(REPO)
                print(f"--- {rel} (with ref image) ---")
                print(prompt.format(identity=identity)[:200] + "...\n")
        return

    client = genai.Client(api_key=API_KEY)
    step = 0

    # ── Pass 1: Generate profiles ──────────────────────────────────────
    if not pass2_only:
        print("═══ PASS 1: Generating profile photos ═══\n")
        for key, person in people.items():
            step += 1
            identity = IDENTITY[key]
            prompt = person["profile_prompt"].format(identity=identity)
            print(f"[{step}/{total}] {key} profile ...")
            generate_image(client, prompt, person["profile_path"])
            time.sleep(5)
    else:
        print("═══ PASS 1: Skipped (--pass2-only) ═══\n")
        step = len(people)

    # ── Pass 2: Generate variants using profile as reference ───────────
    print("\n═══ PASS 2: Generating variants (with profile reference) ═══\n")
    for key, person in people.items():
        profile_path = person["profile_path"]
        if not profile_path.exists():
            print(f"  SKIP {key} variants — profile not found at {profile_path}")
            continue

        ref_bytes = profile_path.read_bytes()
        identity = IDENTITY[key]

        for var_path, var_prompt in person["variants"]:
            step += 1
            prompt = var_prompt.format(identity=identity)
            rel = var_path.relative_to(REPO)
            print(f"[{step}/{total}] {rel} ...")
            generate_image(client, prompt, var_path, ref_image_bytes=ref_bytes)
            time.sleep(5)

    # ── Pass 3: Team photo (using all profiles as reference) ───────────
    if not only:
        step += 1
        print(f"\n═══ PASS 3: Team photo ═══\n")
        team_photo_path = ASSETS_DIR / "team_photo.png"

        # Collect all profile images as reference
        profile_parts = []
        names_order = ["t1_elena", "t2_marco", "t3_kavya", "klean",
                       "t4_kevin", "t5_marcus", "t6_soyeon", "t7_lucas"]
        for name in names_order:
            pp = PEOPLE[name]["profile_path"]
            if pp.exists():
                profile_parts.append(
                    types.Part.from_bytes(data=pp.read_bytes(), mime_type="image/png")
                )

        team_prompt = (
            "The 8 photos above are individual portraits of team members. "
            "Generate a GROUP PHOTO of these EXACT 8 people standing together on an outdoor "
            "tennis court at golden hour. They should look exactly like their portraits. "
            "Left to right order: Elena (Italian woman, auburn hair), Marco (Chinese man, broad shoulders), "
            "Kavya (Indian woman, dark hair in braid, nose stud), Klean (Chinese man, center, confident), "
            "Kevin (Chinese man, tousled hair), Marcus (German man, tall, light brown hair), "
            "Soyeon (Korean woman, shoulder-length black hair), "
            "Lucas (Brazilian man, curly dark hair). All wearing matching black crew-neck t-shirts "
            "with 'Dawnflow' logo. Casual confident team vibe. Green trees behind the court. "
            "Wide shot showing full bodies. Shot on Sony A7IV 24mm f/2.8."
        )

        contents = profile_parts + [team_prompt]
        print(f"[{step}/{total}] Team photo (8 reference images) ...")
        try:
            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["Text", "Image"],
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    team_photo_path.write_bytes(part.inline_data.data)
                    print(f"  OK: team_photo.png ({len(part.inline_data.data):,} bytes)")
                    break
                elif part.text is not None:
                    print(f"  Text: {part.text[:120]}")
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nDone!")


if __name__ == "__main__":
    main()
