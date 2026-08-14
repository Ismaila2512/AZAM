from PIL import Image
import os

img_paths = [
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_0_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_1_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_2_1785843762551.png"
]

images = [Image.open(p).convert("RGB") for p in img_paths]

# 1. CAROUSEL PDF (Highly Recommended for LinkedIn)
# LinkedIn turns PDFs into swipeable carousels which get massively boosted by the algorithm.
images[0].save("/Users/apple/Desktop/Azam_Radar_Carousel.pdf", save_all=True, append_images=images[1:])


# 2. 4:5 OPTIMIZED SINGLE IMAGE 
# A 1080 x 1350 is the max vertical size for LinkedIn before it crops.
target_width = 1080
target_height = 1350
bgColor = (5, 1, 1)

grid = Image.new('RGB', (target_width, target_height), color=bgColor)

# We have 3 images to fit horizontally
# Let's resize each image to be width = 1000 (with 40px padding on edges)
img_width = 1000
processed_imgs = []
for img in images:
    h = int(img.height * (img_width / img.width))
    processed_imgs.append(img.resize((img_width, h), Image.Resampling.LANCZOS))

# Total height of the 3 images
total_img_height = sum(img.height for img in processed_imgs)
# Calculate extra vertical space
remaining_space = target_height - total_img_height
# Distribute padding (top, between 1-2, between 2-3, bottom)
padding = remaining_space // 4

y_offset = padding
for img in processed_imgs:
    # Center horizontally
    x_offset = (target_width - img_width) // 2
    grid.paste(img, (x_offset, y_offset))
    y_offset += img.height + padding

grid.save("/Users/apple/Desktop/Azam_Radar_4x5.png")

print("Generated both PDF and 4x5 Image!")
