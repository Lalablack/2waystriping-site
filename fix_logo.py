#!/usr/bin/env python3
"""Fix logo transparency and create proper square favicon."""

from PIL import Image
import os

# Paths
source_logo = "/home/ubuntu/.cursor/projects/workspace/uploads/2waystriping-logo-from-george-2026-11-09_004f.png"
output_dir = "/workspace/public/images"
output_logo = os.path.join(output_dir, "2way-logo.png")
output_favicon_32 = os.path.join(output_dir, "favicon-32.png")
output_favicon_16 = os.path.join(output_dir, "favicon-16.png")
output_apple = os.path.join(output_dir, "apple-touch-icon.png")

# Load the image
img = Image.open(source_logo)
img = img.convert("RGBA")

# Better white background removal with anti-aliasing preservation
data = img.getdata()
new_data = []
for item in data:
    r, g, b, a = item
    # Calculate how "white" this pixel is
    # Use a more sophisticated approach: make pixels transparent based on how white they are
    if r > 245 and g > 245 and b > 245:
        # Calculate alpha based on how far from pure white
        whiteness = min(r, g, b)
        # If very white (>250), make it fully transparent
        if whiteness > 250:
            new_data.append((255, 255, 255, 0))
        else:
            # Gradually reduce alpha for near-white pixels (handles anti-aliasing)
            new_alpha = max(0, 255 - whiteness)
            new_data.append((r, g, b, new_alpha))
    else:
        new_data.append(item)

img.putdata(new_data)

# Save the main logo
img.save(output_logo, "PNG", optimize=True)
print(f"✓ Main logo: {output_logo}")
print(f"  Size: {os.path.getsize(output_logo)} bytes, {img.size}")

# Create square 32x32 favicon
# The logo is 234x180, aspect ratio ~1.3:1
# Center the logo on a square transparent canvas
logo_32 = img.copy()
logo_32.thumbnail((32, 32), Image.Resampling.LANCZOS)

# Create 32x32 canvas and center the resized logo
favicon_32 = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
x_offset = (32 - logo_32.size[0]) // 2
y_offset = (32 - logo_32.size[1]) // 2
favicon_32.paste(logo_32, (x_offset, y_offset), logo_32)
favicon_32.save(output_favicon_32, "PNG", optimize=True)
print(f"✓ Favicon 32x32: {output_favicon_32}")
print(f"  Size: {os.path.getsize(output_favicon_32)} bytes, {favicon_32.size}")

# Create 16x16 favicon
logo_16 = img.copy()
logo_16.thumbnail((16, 16), Image.Resampling.LANCZOS)
favicon_16 = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
x_offset = (16 - logo_16.size[0]) // 2
y_offset = (16 - logo_16.size[1]) // 2
favicon_16.paste(logo_16, (x_offset, y_offset), logo_16)
favicon_16.save(output_favicon_16, "PNG", optimize=True)
print(f"✓ Favicon 16x16: {output_favicon_16}")
print(f"  Size: {os.path.getsize(output_favicon_16)} bytes, {favicon_16.size}")

# For apple-touch-icon, create a 180x180 square version
logo_180 = img.copy()
logo_180.thumbnail((180, 180), Image.Resampling.LANCZOS)
apple_icon = Image.new('RGBA', (180, 180), (0, 0, 0, 0))
x_offset = (180 - logo_180.size[0]) // 2
y_offset = (180 - logo_180.size[1]) // 2
apple_icon.paste(logo_180, (x_offset, y_offset), logo_180)
apple_icon.save(output_apple, "PNG", optimize=True)
print(f"✓ Apple touch icon 180x180: {output_apple}")
print(f"  Size: {os.path.getsize(output_apple)} bytes, {apple_icon.size}")
