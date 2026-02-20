"""
Process INCBA logos:
1. Remove background (make transparent) from both versions
2. Auto-crop whitespace/empty area
3. Re-embed into HTML proposal
"""
import base64
from io import BytesIO
from PIL import Image
import os

root = r'd:\GITHUB\recursos-humanos-norpan'


def remove_background(img_path, bg_threshold=30, corner_sample=True):
    """Remove background from PNG, making it transparent.
    
    Detects the dominant background color from corners,
    then makes all similar pixels transparent.
    """
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    w, h = img.size
    
    # Sample background color from corners (20px squares)
    corner_pixels = []
    for x in range(20):
        for y in range(20):
            corner_pixels.append(img.getpixel((x, y))[:3])                  # top-left
            corner_pixels.append(img.getpixel((w - 1 - x, y))[:3])          # top-right
            corner_pixels.append(img.getpixel((x, h - 1 - y))[:3])          # bottom-left
            corner_pixels.append(img.getpixel((w - 1 - x, h - 1 - y))[:3]) # bottom-right
    
    # Average background color
    avg_r = sum(p[0] for p in corner_pixels) // len(corner_pixels)
    avg_g = sum(p[1] for p in corner_pixels) // len(corner_pixels)
    avg_b = sum(p[2] for p in corner_pixels) // len(corner_pixels)
    
    print(f"  Detected BG color: rgb({avg_r}, {avg_g}, {avg_b})")
    
    # Replace similar pixels with transparent
    new_data = []
    for item in data:
        r, g, b, a = item
        # Distance from background color
        dist = ((r - avg_r) ** 2 + (g - avg_g) ** 2 + (b - avg_b) ** 2) ** 0.5
        if dist < bg_threshold:
            new_data.append((r, g, b, 0))  # Fully transparent
        elif dist < bg_threshold * 2:
            # Semi-transparent for anti-aliased edges
            alpha = int(min(255, (dist - bg_threshold) / bg_threshold * 255))
            new_data.append((r, g, b, alpha))
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img


def auto_crop(img, padding=20):
    """Crop to content bounding box + padding."""
    # Find bounding box of non-transparent pixels
    bbox = img.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(img.width, right + padding)
        bottom = min(img.height, bottom + padding)
        img = img.crop((left, top, right, bottom))
    return img


def img_to_base64(img):
    """Convert PIL Image to base64 PNG string."""
    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


# Process both logos
print("Processing incba_claro.png (dark text, for light backgrounds)...")
claro = remove_background(os.path.join(root, 'incba_claro.png'), bg_threshold=35)
claro = auto_crop(claro)
claro_b64 = img_to_base64(claro)
print(f"  Result: {claro.width}x{claro.height}, {len(claro_b64)} chars base64\n")

print("Processing incba_oscuro.png (light text, for dark backgrounds)...")
oscuro = remove_background(os.path.join(root, 'incba_oscuro.png'), bg_threshold=35)
oscuro = auto_crop(oscuro)
oscuro_b64 = img_to_base64(oscuro)
print(f"  Result: {oscuro.width}x{oscuro.height}, {len(oscuro_b64)} chars base64\n")

# Save processed PNGs for reference
claro.save(os.path.join(root, 'incba_claro_transparent.png'))
oscuro.save(os.path.join(root, 'incba_oscuro_transparent.png'))
print("Saved transparent PNGs for reference.")

# Now update the HTML
html_path = os.path.join(root, 'docs', 'propuesta-pulso-norpan.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

oscuro_uri = f'data:image/png;base64,{oscuro_b64}'
claro_uri = f'data:image/png;base64,{claro_b64}'

# Find and replace all existing data:image/png;base64 in src attributes
import re

# Find all img tags with data URIs
img_tags = list(re.finditer(r'<img\s+src="data:image/png;base64,[^"]*"([^>]*)>', html))
print(f"\nFound {len(img_tags)} embedded images in HTML")

for i, m in enumerate(img_tags):
    attrs = m.group(1)
    print(f"  Image {i}: ...{attrs.strip()[:80]}")

# Strategy:
# - Cover logo (slide-cover, class="cover-logo") → oscuro (light text on transparent)
# - CTA slide logo (last section, class="cover-logo") → oscuro
# - Footer logo (class="footer-logo") → oscuro
# All are on dark backgrounds → use oscuro

# Replace all logo sources (data URIs or relative file paths) with oscuro version
# Since all 3 logos are on dark backgrounds, all should use oscuro
pattern_data = r'src="data:image/png;base64,[^"]*"'
pattern_file = r'src="\.\./incba_(?:oscuro|claro)\.png"'
html_new = re.sub(pattern_data, f'src="{oscuro_uri}"', html)
count1 = len(re.findall(pattern_data, html))
html_new = re.sub(pattern_file, f'src="{oscuro_uri}"', html_new)
count2 = len(re.findall(pattern_file, html))
replacements = count1 + count2
print(f"\nReplaced {replacements} image sources with transparent oscuro logo (data:{count1}, file:{count2})")

with open(html_path, 'w', encoding='utf-8') as f:
    f_write = f.write(html_new)

size_kb = os.path.getsize(html_path) / 1024
print(f"HTML updated. Size: {size_kb:.0f} KB")
print("Done!")
