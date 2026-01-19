import os
import math
from PIL import Image, ImageEnhance, ImageOps

# ================= CONFIG =================
BASE_IMAGE = "hackerbot_base.png"
OUTPUT_ROOT = "../mascot"

SIZE = (96, 96)

ACTIONS = {
    "idle": 4,
    "walk": 6,
    "run": 6,
    "fly": 6,
    "learn": 4,
    "think": 3,
    "alert": 3,
    "code": 4,
    "drone": 4,
    "capsule": 2,
}

SKINS = {
    "hackerbot": {"brightness": 1.0, "color_shift": None},
    "hackerbot_stealth": {"brightness": 0.8, "color_shift": "green"},
}
# =========================================


def ensure_dirs():
    for skin in SKINS:
        for action in ACTIONS:
            for direction in ("right", "left"):
                os.makedirs(
                    os.path.join(OUTPUT_ROOT, skin, action, direction),
                    exist_ok=True
                )


def load_base():
    img = Image.open(BASE_IMAGE).convert("RGBA")
    return img.resize(SIZE, Image.LANCZOS)


# ================= TRANSFORMS =================

def brightness(img, factor):
    return ImageEnhance.Brightness(img).enhance(factor)


def rotate(img, deg):
    return img.rotate(deg, resample=Image.BICUBIC, expand=False)


def translate(img, dx, dy):
    bg = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    bg.paste(img, (dx, dy), img)
    return bg


def flip(img):
    return ImageOps.mirror(img)


def eye_boost(img, intensity):
    # Simple boost global (ojos ya son verdes en la imagen)
    return ImageEnhance.Contrast(img).enhance(1 + intensity)


# ================= GENERATOR =================

def generate_action(base, skin_cfg, action, frames):
    for i in range(frames):
        img = base.copy()

        # ---- acción base ----
        if action == "idle":
            img = rotate(img, math.sin(i) * 1.5)

        elif action == "walk":
            img = translate(img, int(math.sin(i) * 3), 0)

        elif action == "run":
            img = translate(img, int(math.sin(i) * 6), 0)

        elif action == "fly":
            img = translate(img, int(math.sin(i) * 4), int(math.cos(i) * -4))

        elif action == "learn":
            img = eye_boost(img, 0.4)

        elif action == "think":
            img = rotate(img, (-1) ** i * 2)

        elif action == "alert":
            img = eye_boost(img, 0.8 if i % 2 == 0 else 0.2)

        elif action == "code":
            img = translate(img, 0, 2)

        elif action == "drone":
            img = rotate(img, math.sin(i) * 3)

        elif action == "capsule":
            img = brightness(img, 0.6)

        # ---- skin ----
        img = brightness(img, skin_cfg["brightness"])

        # ---- save right + left ----
        yield img, flip(img)


def main():
    ensure_dirs()
    base = load_base()

    for skin, cfg in SKINS.items():
        for action, frames in ACTIONS.items():
            for i, (right, left) in enumerate(
                generate_action(base, cfg, action, frames)
            ):
                right.save(
                    os.path.join(
                        OUTPUT_ROOT, skin, action, "right",
                        f"{action}_{i+1}.png"
                    )
                )
                left.save(
                    os.path.join(
                        OUTPUT_ROOT, skin, action, "left",
                        f"{action}_{i+1}.png"
                    )
                )

    print("✅ Sprites avanzados generados correctamente.")


if __name__ == "__main__":
    main()
