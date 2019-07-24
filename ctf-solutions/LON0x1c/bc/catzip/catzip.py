import PIL.ImageStat

from gridimage import AmbiguousImageSegmentError, main


def cat_emoji_decoder(region):
    data = PIL.ImageStat.Stat(region)
    if data.sum == [396994.0, 361811.0, 269950.0]:
        return "0"
    elif data.sum == [400404.0, 340942.0, 264680.0]:
        return "1"
    raise AmbiguousImageSegmentError


if __name__ == '__main__':
    main(cat_emoji_decoder)
