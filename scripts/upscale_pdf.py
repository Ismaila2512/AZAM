from reportlab.pdfgen import canvas
from PIL import Image, ImageEnhance
import os

img_paths = [
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_0_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_1_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_2_1785843762551.png"
]

pdf_path = "/Users/apple/Desktop/Azam_Radar_Carousel_4K.pdf"

c = canvas.Canvas(pdf_path)

for idx, path in enumerate(img_paths):
    img = Image.open(path).convert('RGB')
    
    # Scale exactly 2.5x to reach ~2560px width
    new_width = int(img.width * 2.5)
    new_height = int(img.height * 2.5)
    
    # Use extremely high quality upsampling
    img_upscaled = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Enhance Image Sharpness to prevent pixel bleeding
    enhancer = ImageEnhance.Sharpness(img_upscaled)
    img_sharp = enhancer.enhance(1.5)
    
    # Enhance Contrast slightly
    enhancer2 = ImageEnhance.Contrast(img_sharp)
    img_final = enhancer2.enhance(1.05)
    
    # Save the huge temporary image so ReportLab can ingest it as a pure PNG stream
    temp_name = f"temp_upscaled_{idx}.png"
    img_final.save(temp_name, optimize=False)
    
    # Draw huge canvas
    c.setPageSize((new_width, new_height))
    c.drawImage(temp_name, 0, 0, width=new_width, height=new_height)
    c.showPage()
    
    # clean up
    os.remove(temp_name)

c.save()
print("Saved 4K PDF!")
