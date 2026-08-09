import argparse
from PIL import Image, ImageDraw
import os
import sys

def draw_grid(input_path, output_path, spacing):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)
        
    try:
        img = Image.open(input_path).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw horizontal lines
        for y in range(0, img.height, spacing):
            draw.line([(0, y), (img.width, y)], fill=(255, 0, 0), width=1)
            draw.text((10, y), str(y), fill=(255, 255, 0))
            
        img.save(output_path)
        print(f"Success! Grid overlay written to: {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Draw a coordinate grid over an image.")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to save output image")
    parser.add_argument("--spacing", type=int, default=20, help="Grid spacing in pixels (default: 20)")
    
    args = parser.parse_args()
    draw_grid(args.input, args.output, args.spacing)

if __name__ == "__main__":
    main()
