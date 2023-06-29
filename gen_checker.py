import argparse
from PIL import Image
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_checkerboard(width, height):
    image = Image.new("RGB", (width, height))

    color_a = WHITE
    color_b = BLACK

    for y in range(height):
        color_temp = color_a
        color_a = color_b
        color_b = color_temp

        for x in range(width):
            color = color_a if x % 2 == 0 else color_b
            image.putpixel((x, y), color)

    return image

def main():
    parser = argparse.ArgumentParser(description="Generate a checkerboard image.")
    parser.add_argument("--width", type=int, help="Width of the checkerboard image")
    parser.add_argument("--height", type=int, help="Height of the checkerboard image")
    parser.add_argument("--output", type=str, help="Output file path for the generated image")
    args = parser.parse_args()

    width = args.width or 8
    height = args.height or 8

    if width <= 0 or height <= 0:
        print("Width and height must be positive integers.", file=sys.stderr)
        sys.exit(1)

    if not args.output:
        print("No output file specified. Please provide an output file path using the --output option.", file=sys.stderr)
        sys.exit(1)

    output_file = args.output
    if not output_file.endswith(".png"):
        output_file += ".png"

    image = generate_checkerboard(width, height)
    image.save(output_file, format="PNG")
    print(f"Checkerboard image saved to: {output_file}")

if __name__ == "__main__":
    main()
