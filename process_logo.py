#!/usr/bin/env python3
"""Process the 2 Way Striping logo: make white background transparent and create favicon."""

from PIL import Image
import os

# Paths
source_logo = "/home/ubuntu/.cursor/projects/workspace/uploads/2waystriping-logo-from-george-2026-11-09_004f.png"
output_dir = "/workspace/public/images"
output_logo = os.path.join(output_dir, "2way-logo.png")
output_favicon = os.path.join(output_dir, "2way-favicon.png")

# Load the image
img = Image.open(source_logo)
img = img.convert("RGBA")

# Get image data
data = img.getdata()

# Replace white background with transparent
new_data = []
for item in data:
    # If the pixel is very close to white (R, G, B all > 250), make it transparent
    if item[0] > 250 and item[1] > 250 and item[2] > 250:
        new_data.append((255, 255, 255, 0))  # Transparent
    else:
        new_data.append(item)

img.putdata(new_data)

# Save the main logo (optimized)
img.save(output_logo, "PNG", optimize=True)
print(f"Saved main logo: {output_logo}")
print(f"  Original size: {os.path.getsize(source_logo)} bytes")
print(f"  New size: {os.path.getsize(output_logo)} bytes")
print(f"  Dimensions: {img.size}")

# Create favicon (32x32) - use the red worker figure as the main element
# The logo is 234x180, so we'll resize maintaining aspect ratio and then crop/center
favicon = img.copy()
# Resize to fit in 32x32 while maintaining aspect ratio
favicon.thumbnail((32, 32), Image.Resampling.LANCZOS)
favicon.save(output_favicon, "PNG", optimize=True)
print(f"\nSaved favicon: {output_favicon}")
print(f"  Size: {os.path.getsize(output_favicon)} bytes")
print(f"  Dimensions: {favicon.size}")

# For apple-touch-icon, create a 180x180 version
apple_icon = img.copy()
apple_icon.thumbnail((180, 180), Image.Resampling.LANCZOS)
output_apple = os.path.join(output_dir, "apple-touch-icon.png")
apple_icon.save(output_apple, "PNG", optimize=True)
print(f"\nSaved apple-touch-icon: {output_apple}")
print(f"  Size: {os.path.getsize(output_apple)} bytes")
print(f"  Dimensions: {apple_icon.size}")
