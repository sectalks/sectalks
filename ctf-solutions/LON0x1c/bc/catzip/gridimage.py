import argparse
import math

import PIL.ImageStat

from PIL import Image


class AmbiguousImageSegmentError(Exception):
    pass


def parse_image(image, width, height, tmp_file, decoder):
    columns = image.size[0] // width
    rows = image.size[1] // height
    for row in range(rows):
        for column in range(columns):
            box = (
                column * width,
                row * height,
                (column + 1) * width,
                (row + 1) * height,
            )
            region = image.crop(box)
            try:
                yield decoder(region)
            except AmbiguousImageSegmentError:
                threshold = 200
                if min(width, height) < threshold:
                    if width < height:
                        region.resize((threshold, (height * threshold) // width)).save("current.png")
                    else:
                        region.resize((((width * threshold) // height), threshold)).save("current.png")
                else:
                    region.save(tmp_file)
                ask = input(f"Check {tmp_file}. Value for ({column},{row}): ")
                if ask == "quit":
                    return
                yield ask


def run(image, glyph_width, glyph_height, tmp_file, decoder):
    print("".join(list(parse_image(image, glyph_width, glyph_height, tmp_file, decoder))))


def main(decoder):
    parser = argparse.ArgumentParser()
    parser.add_argument("image_file")
    x_group = parser.add_mutually_exclusive_group(required=True)
    x_group.add_argument("-x", "--width", type=int)
    x_group.add_argument("-c", "--cols", "--columns", type=int)
    x_group.add_argument("--width-same-as-height", action='store_true')
    y_group = parser.add_mutually_exclusive_group(required=True)
    y_group.add_argument("-y", "--height", type=int)
    y_group.add_argument("-r", "--rows", type=int)
    y_group.add_argument("--height-same-as-width", action='store_true')
    parser.add_argument("--y-offset", type=int, default=0)
    parser.add_argument("--x-offset", type=int, default=0)
    parser.add_argument("--y-offset-bottom", type=int, default=0)
    parser.add_argument("--x-offset-left", type=int, default=0)
    parser.add_argument(
        "--tmp-file", default="current.png", help="Write region here if it's too ambiguous to decode",
    )
    args = parser.parse_args()
    image = Image.open(args.image_file)
    full_width, full_height = image.size
    full_width -= args.x_offset_left
    full_height -= args.y_offset_bottom
    cropped = image.crop((args.x_offset, args.y_offset, full_width, full_height))
    if args.width:
        width = args.width
    elif args.cols:
        width = int((full_width + 0.5) / args.cols)
    if args.height:
        height = args.height
    elif args.rows:
        height = int((full_height + 0.5) / args.rows)
    if args.width_same_as_height:
        assert height
        width = height
    if args.height_same_as_width:
        assert width
        height = width
    run(
        cropped,
        width,
        height,
        args.tmp_file,
        decoder,
    )
