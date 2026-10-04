"""
Generates high-resolution diagnostic sample leaf images for the Multi-Modal Vision Scanner.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("assets/samples", exist_ok=True)

# 1. Healthy Paddy Leaf
img_healthy = Image.new("RGB", (400, 300), color=(15, 23, 42))
draw = ImageDraw.Draw(img_healthy)
# Leaf blade polygon
draw.polygon([(60, 260), (140, 40), (200, 20), (260, 40), (340, 260)], fill=(34, 197, 94))
# Leaf midrib & veins
draw.line([(200, 20), (200, 260)], fill=(74, 222, 128), width=3)
for y in range(40, 240, 25):
    draw.line([(200, y), (140, y + 20)], fill=(74, 222, 128), width=1)
    draw.line([(200, y), (260, y + 20)], fill=(74, 222, 128), width=1)
img_healthy = img_healthy.filter(ImageFilter.SMOOTH)
img_healthy.save("assets/samples/healthy_paddy.png")

# 2. Rice Blast (Spindle-shaped grey-brown necrotic lesions)
img_blast = Image.new("RGB", (400, 300), color=(15, 23, 42))
draw = ImageDraw.Draw(img_blast)
draw.polygon([(60, 260), (140, 40), (200, 20), (260, 40), (340, 260)], fill=(74, 160, 80))
draw.line([(200, 20), (200, 260)], fill=(50, 120, 60), width=3)
# Spindle lesions with grey centers and brown borders
lesions = [(180, 80, 220, 130), (150, 140, 190, 190), (210, 160, 250, 220), (190, 210, 230, 250)]
for x1, y1, x2, y2 in lesions:
    draw.ellipse([x1-4, y1-4, x2+4, y2+4], fill=(120, 53, 15))  # Brown border
    draw.ellipse([x1, y1, x2, y2], fill=(156, 163, 175))       # Grey necrotic center
img_blast = img_blast.filter(ImageFilter.SMOOTH)
img_blast.save("assets/samples/rice_blast.png")

# 3. Cashew Dieback / Inflorescence Blight (Scorched tips and black necrotic patches)
img_cashew = Image.new("RGB", (400, 300), color=(15, 23, 42))
draw = ImageDraw.Draw(img_cashew)
# Broad oval cashew leaf
draw.ellipse([(100, 40), (300, 260)], fill=(101, 163, 13))
# Tip blight (withered dark brown scorched region)
draw.chord([(100, 40), (300, 140)], start=0, end=360, fill=(69, 26, 3))
# Necrotic spotting
for (cx, cy, r) in [(180, 140, 14), (220, 170, 18), (160, 190, 12), (240, 210, 10)]:
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(30, 20, 10))
img_cashew = img_cashew.filter(ImageFilter.SMOOTH)
img_cashew.save("assets/samples/cashew_dieback.png")

# 4. Coconut Bud Rot (Yellowing frond + central black water-soaked decay)
img_budrot = Image.new("RGB", (400, 300), color=(15, 23, 42))
draw = ImageDraw.Draw(img_budrot)
# Radiating palm fronds
for angle in range(-45, 50, 15):
    rad = np.radians(angle)
    ex = int(200 + 170 * np.sin(rad))
    ey = int(260 - 220 * np.cos(rad))
    draw.line([(200, 260), (ex, ey)], fill=(234, 179, 8), width=6)  # Chlorotic yellow fronds
# Central rotting heart / spear leaf
draw.polygon([(180, 260), (195, 80), (205, 80), (220, 260)], fill=(24, 24, 27))  # Rotting black spear leaf
img_budrot = img_budrot.filter(ImageFilter.SMOOTH)
img_budrot.save("assets/samples/coconut_bud_rot.png")

print("Created 4 sample leaf pathology images in assets/samples/")
