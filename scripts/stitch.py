from PIL import Image
import os

img_paths = [
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_0_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_1_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_2_1785843762551.png"
]

images = [Image.open(p) for p in img_paths]

# Find the maximum width
max_width = max(img.width for img in images)

# Resize all images to the maximum width to keep things proportional
processed_images = []
for img in images:
    if img.width != max_width:
        new_height = int(img.height * (max_width / img.width))
        processed_images.append(img.resize((max_width, new_height), Image.Resampling.LANCZOS))
    else:
        processed_images.append(img)

# padding between images
padding = 40
total_height = sum(img.height for img in processed_images) + padding * (len(processed_images) - 1)

# Create a new blank canvas (black background to match UI)
collage = Image.new('RGB', (max_width, total_height), color=(5, 1, 1))

y_offset = 0
for img in processed_images:
    collage.paste(img, (0, y_offset))
    y_offset += img.height + padding

collage.save("/Users/apple/Desktop/Azam_Radar_LinkedIn_Post.png")
print("Saved to Desktop!")
