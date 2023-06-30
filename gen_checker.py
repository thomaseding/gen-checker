import argparse
import os
import sys
from PIL import Image
from typing import Optional, Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_checkerboard(*, width: int, height: int, upscale_width: Optional[int] = None, upscale_height: Optional[int] = None) -> Image.Image:
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

    if upscale_width is not None and upscale_height is not None:
        image = image.resize((upscale_width, upscale_height), Image.NEAREST)
    else:
        assert upscale_width is None and upscale_height is None

    return image

def generate_checkerboard_image(*, width: int, height: int, output_file: str, upscale_width: Optional[int], upscale_height: Optional[int]) -> None:
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    assert output_file.lower().endswith(".png")
    image = generate_checkerboard(width=width, height=height, upscale_width=upscale_width, upscale_height=upscale_height)
    image.save(output_file, format="PNG")
    print(f"Checkerboard image saved to: {output_file}")

def generate_checkerboards_in_directory(*, input_dir: str, output_dir: str) -> None:
    if not os.path.isdir(input_dir):
        raise ValueError(f"Invalid input directory: {input_dir}")
    if not os.path.isdir(output_dir):
        raise ValueError(f"Invalid output directory: {output_dir}")

    png_files = [file for file in os.listdir(input_dir) if file.lower().endswith(".png")]
    for png_file in png_files:
        input_path = os.path.join(input_dir, png_file)
        output_path = os.path.join(output_dir, png_file)
        width, height = get_image_dimensions(input_path)
        generate_checkerboard_image(width=width, height=height, output_file=output_path, upscale_width=width, upscale_height=height)

def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    image = Image.open(image_path)
    return image.width, image.height

def parse_dimensions(dimensions: str) -> Tuple[int, int]:
    try:
        width, height = [int(dim) for dim in dimensions.split("x")]
    except ValueError:
        raise ValueError("Invalid dimensions. Dimensions must be in the format <width>x<height>.")
    return width, height

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a checkerboard image or generate checkers for PNG images in a directory.")
    parser.add_argument("--dims", type=str, help="Dimensions of the checkerboard image in the format <width>x<height>")
    parser.add_argument("--input-dir", type=str, help="Input directory path for PNG images")
    parser.add_argument("--output-dir", type=str, help="Output directory path for generated checker images")
    parser.add_argument("--output-file", type=str, help="Output file path for generated checker image")
    parser.add_argument("--upscale-dims", type=str, help="Upscale dimensions of the checkerboard image in the format <width>x<height>")
    args = parser.parse_args()

    args.width = None
    args.height = None
    if args.dims:
        args.width, args.height = parse_dimensions(args.dims)

    args.upscale_width = None
    args.upscale_height = None
    if args.upscale_dims:
        args.upscale_width, args.upscale_height = parse_dimensions(args.upscale_dims)

    if args.input_dir and args.output_dir:
        if args.output_file:
            raise ValueError("Output file cannot be specified when generating checkers for PNG images in a directory.")
        if args.width is not None or args.height is not None:
            raise ValueError("Width and height cannot be specified when generating checkers for PNG images in a directory.")
        generate_checkerboards_in_directory(input_dir=args.input_dir, output_dir=args.output_dir)
    elif args.output_file and args.width and args.height:
        if args.input_dir or args.output_dir:
            raise ValueError("Both input and output directories must be specified when generating checkers for PNG images in a directory.")
        if not args.output_file:
            raise ValueError("Output file must be specified when generating a single checkerboard image.")
        generate_checkerboard_image(width=args.width, height=args.height, output_file=args.output_file, upscale_width=args.upscale_width, upscale_height=args.upscale_height)
    else:
        raise ValueError("Invalid arguments. See --help for more information.")

if __name__ == "__main__":
    main()
