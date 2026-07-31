import argparse
from PIL import Image
import os
import sys

def stitch_screenshot(input_path, output_path, keep_ranges):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)
        
    try:
        img = Image.open(input_path).convert('RGB')
        w, h = img.size
        
        # Parse keep ranges
        ranges = []
        for r in keep_ranges:
            try:
                start, end = map(int, r.split('-'))
                # Clamp to image height
                start = max(0, start)
                end = min(h, end)
                if start >= end:
                    print(f"Warning: Invalid range {r} (start >= end). Skipping.")
                    continue
                ranges.append((start, end))
            except ValueError:
                print(f"Error: Invalid range format '{r}'. Expected 'start-end' (e.g. '0-40').")
                sys.exit(1)
                
        if not ranges:
            print("Error: No valid ranges provided.")
            sys.exit(1)
            
        # Crop slices
        slices = []
        total_height = 0
        for start, end in ranges:
            s = img.crop((0, start, w, end))
            slices.append(s)
            total_height += s.height
            
        # Stitch
        new_img = Image.new('RGB', (w, total_height))
        current_y = 0
        for s in slices:
            new_img.paste(s, (0, current_y))
            current_y += s.height
            
        new_img.save(output_path)
        print(f"Success! Stitched screenshot written to: {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Stitch specific Y-coordinate horizontal slices of an image.")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to save output image")
    parser.add_argument("--keep-ranges", nargs='+', required=True, help="List of Y-coordinate ranges to keep, in format 'start-end' (e.g. '0-40' '285-545')")
    
    args = parser.parse_args()
    stitch_screenshot(args.input, args.output, args.keep_ranges)

if __name__ == "__main__":
    main()
