from PIL import Image
from io import BytesIO
from typing import List


def bytes_to_image(data: bytes) -> Image.Image:
    """
    Convert raw PNG bytes to a PIL Image object.
    """
    return Image.open(BytesIO(data))


def image_to_bytes(img: Image.Image, format: str = "PNG") -> bytes:
    """
    Convert a PIL Image to raw bytes in the specified format (default PNG).
    """
    buf = BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def split_image(img: Image.Image, num_parts: int) -> List[bytes]:
    """
    Split the input image into `num_parts` horizontal stripes,
    returning a list of raw PNG bytes for each segment.
    """
    width, height = img.size
    part_height = height // num_parts
    segments: List[bytes] = []
    for i in range(num_parts):
        top = i * part_height
        bottom = (i + 1) * part_height if i < num_parts - 1 else height
        box = (0, top, width, bottom)
        segment = img.crop(box)
        segments.append(image_to_bytes(segment))
    return segments


def reconstruct_image(segments: List[bytes]) -> bytes:
    """
    Reconstruct a full grayscale image from a list of segment bytes (PNG),
    returning raw PNG bytes of the combined image.
    """
    # Convert each segment bytes back to PIL Image
    imgs = [bytes_to_image(b) for b in segments]
    widths, heights = zip(*(im.size for im in imgs))
    total_height = sum(heights)
    max_width = max(widths)

    # Create new grayscale image to paste segments
    output = Image.new("L", (max_width, total_height))
    y_offset = 0
    for im in imgs:
        output.paste(im, (0, y_offset))
        y_offset += im.height

    return image_to_bytes(output)


def convert_chunk(data: bytes) -> bytes:
    """
    Convert a raw PNG bytes chunk to grayscale,
    returning raw PNG bytes of the processed chunk.
    """
    img = bytes_to_image(data).convert("L")
    return image_to_bytes(img)
