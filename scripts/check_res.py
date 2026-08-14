from PIL import Image
import os

img_paths = [
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_0_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_1_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_2_1785843762551.png"
]

for p in img_paths:
    img = Image.open(p)
    print(f"{os.path.basename(p)}: {img.size}")
