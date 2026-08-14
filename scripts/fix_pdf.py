from reportlab.pdfgen import canvas
from PIL import Image
import os

img_paths = [
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_0_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_1_1785843762551.png",
    "/Users/apple/.gemini/antigravity/brain/80a24f41-f553-4752-9e58-bc1f86612293/uploaded_media_2_1785843762551.png"
]

pdf_path = "/Users/apple/Desktop/Azam_Radar_Carousel_HD.pdf"

# Initialize canvas with dummy size, will overwrite per page
c = canvas.Canvas(pdf_path)

for path in img_paths:
    img = Image.open(path)
    # Using 1 point = 1 pixel
    w, h = img.size
    
    # Set page size to exact image dimensions
    c.setPageSize((w, h))
    
    # Draw image at 0,0 with exact native dimensions
    # This prevents any DPI scaling or compression blur
    c.drawImage(path, 0, 0, width=w, height=h)
    c.showPage()
    
c.save()
print("Saved HD PDF!")
