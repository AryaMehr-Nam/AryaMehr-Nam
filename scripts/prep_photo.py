import sys
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def prep_photo(input_path: str = "me.jpg", output_path: str = "source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"[info] File '{input_path}' not found. Skipping photo prep.")
        return False

    with open(input_path, "rb") as f:
        raw_bytes = f.read()

    # 1. Try subject isolation with rembg if installed
    try:
        from rembg import remove
        cutout_bytes = remove(raw_bytes)
        img = Image.open(BytesIO(cutout_bytes)).convert("RGBA")
        print("[ok] Background processed via rembg.")
    except Exception as e:
        print(f"[info] rembg not used ({e}); processing original image directly.")
        img = Image.open(BytesIO(raw_bytes)).convert("RGBA")

    # 2. Composite onto clean contrast base
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, img).convert("L")
    gray_np = np.array(composited)

    # 3. CLAHE local contrast enhancement (eyes, facial contours, glasses)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrast_np = clahe.apply(gray_np)

    # 4. Unsharp masking so fine edges stay sharp in ASCII grid
    gaussian = cv2.GaussianBlur(contrast_np, (0, 0), 2.0)
    sharpened_np = cv2.addWeighted(contrast_np, 1.4, gaussian, -0.4, 0)

    # If alpha was present, clear background to white
    alpha_mask = np.array(img.split()[-1])
    sharpened_np[alpha_mask < 25] = 255

    cv2.imwrite(output_path, sharpened_np)
    print(f"[ok] Saved prepped image to {output_path}")
    return True

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "me.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    prep_photo(src, out)
