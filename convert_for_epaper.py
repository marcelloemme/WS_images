#!/usr/bin/env python3
"""
Simple E-Paper Converter for GitHub Actions
Drop an image in the repo, this converts it automatically.

Usage as GitHub Action:
  python convert_for_epaper.py input.jpg output.bmp
"""

import sys
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path

# 7-color palette (theoretical RGB values for BMP output)
PALETTE = np.array([
    [0, 0, 0],        # Black
    [255, 255, 255],  # White  
    [0, 128, 0],      # Green
    [0, 0, 255],      # Blue
    [255, 0, 0],      # Red
    [255, 255, 0],    # Yellow
    [255, 128, 0],    # Orange
], dtype=np.float64)

# Measured palette (what actually appears on e-paper)
MEASURED = np.array([
    [0, 0, 0],
    [255, 255, 255],
    [0, 100, 0],
    [0, 0, 180],
    [180, 0, 0],
    [200, 200, 0],
    [200, 100, 0],
], dtype=np.float64) / 255.0


def resize_crop(img, w=800, h=480):
    """Resize and center-crop to target dimensions."""
    img = img.convert('RGB')
    ratio = w / h
    img_ratio = img.width / img.height
    
    if img_ratio > ratio:
        new_h = h
        new_w = int(img.width * new_h / img.height)
    else:
        new_w = w
        new_h = int(img.height * new_w / img.width)
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return img.crop((left, top, left + w, top + h))


def enhance(img, saturation=1.5):
    """Boost saturation to compensate for e-paper."""
    return ImageEnhance.Color(img).enhance(saturation)


def dither(pixels, palette):
    """Floyd-Steinberg dithering with measured palette."""
    h, w, _ = pixels.shape
    indices = np.zeros((h, w), dtype=np.uint8)
    
    for y in range(h):
        for x in range(w):
            old = pixels[y, x].copy()
            idx = np.argmin(np.sum((palette - old) ** 2, axis=1))
            indices[y, x] = idx
            new = palette[idx]
            err = old - new
            
            if x + 1 < w:
                pixels[y, x+1] += err * 7/16
            if y + 1 < h:
                if x > 0:
                    pixels[y+1, x-1] += err * 3/16
                pixels[y+1, x] += err * 5/16
                if x + 1 < w:
                    pixels[y+1, x+1] += err * 1/16
    
    return indices


def convert(input_path, output_path, width=800, height=480, saturation=1.5):
    """Convert image for e-paper display."""
    # Load and process
    img = Image.open(input_path)
    img = resize_crop(img, width, height)
    img = enhance(img, saturation)
    
    # Dither
    pixels = np.array(img).astype(np.float64) / 255.0
    indices = dither(pixels, MEASURED)
    
    # Create output image
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(len(PALETTE)):
        result[indices == i] = PALETTE[i].astype(np.uint8)
    
    Image.fromarray(result).save(output_path)
    print(f"✓ Converted: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python convert_for_epaper.py input.jpg output.bmp")
        sys.exit(1)
    
    convert(sys.argv[1], sys.argv[2])
