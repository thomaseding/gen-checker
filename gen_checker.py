import argparse
import os
import sys
from PIL import Image
from typing import Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_checkerboard(width: int, height: int) -> Image:
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

def generate_checkerboard_image(width: int, height: int, output_file: str) -> None:
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    assert output_file.lower().endswith(".png")
    image = generate_checkerboard(width, height)
    image.save(output_file, format="PNG")
    print(f"Checkerboard image saved to: {output_file}")

def generate_checkerboards_in_directory(input_dir: str, output_dir: str) -> None:
    if not os.path.isdir(input_dir):
        raise ValueError(f"Invalid input directory: {input_dir}")
    if not os.path.isdir(output_dir):
        raise ValueError(f"Invalid output directory: {output_dir}")

    png_files = [file for file in os.listdir(input_dir) if file.lower().endswith(".png")]
    for png_file in png_files:
        input_path = os.path.join(input_dir, png_file)
        output_path = os.path.join(output_dir, png_file)
        width, height = get_image_dimensions(input_path)
        generate_checkerboard_image(width, height, output_path)

def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    image = Image.open(image_path)
    return image.width, image.height

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a checkerboard image or generate checkers for PNG images in a directory.")
    parser.add_argument("--width", type=int, help="Width of the checkerboard image")
    parser.add_argument("--height", type=int, help="Height of the checkerboard image")
    parser.add_argument("--input-dir", type=str, help="Input directory path for PNG images")
    parser.add_argument("--output-dir", type=str, help="Output directory path for generated checker images")
    parser.add_argument("--output-file", type=str, help="Output file path for generated checker image")
    args = parser.parse_args()

    if args.input_dir and args.output_dir:
        if args.output_file:
            raise ValueError("Output file cannot be specified when generating checkers for PNG images in a directory.")
        if args.width is not None or args.height is not None:
            raise ValueError("Width and height cannot be specified when generating checkers for PNG images in a directory.")
        generate_checkerboards_in_directory(args.input_dir, args.output_dir)
    elif args.output_file and args.width and args.height:
        if args.input_dir or args.output_dir:
            raise ValueError("Both input and output directories must be specified when generating checkers for PNG images in a directory.")
        if not args.output_dir:
            raise ValueError("No output directory specified. Please provide an output directory path using the --output-dir option.")

        output_dir = args.output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        generate_checkerboard_image(args.width, args.height, args.output_file)
    else:
        raise ValueError("Invalid arguments. See --help for more information.")

if __name__ == "__main__":
    main()
