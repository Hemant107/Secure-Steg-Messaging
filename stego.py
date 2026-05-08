from PIL import Image

HEADER_SIZE = 32  # bits for message length (in bytes)

def _int_to_bits(n, bits):
    return [(n >> i) & 1 for i in range(bits - 1, -1, -1)]

def _bytes_to_bits(data: bytes):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1

def _bits_to_bytes(bits):
    b = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        b.append(byte)
    return bytes(b)

def capacity_in_bits(img: Image.Image):
    w, h = img.size
    return w * h * 3

def encode_bytes_into_image(image_path, data_bytes: bytes, out_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    data_len = len(data_bytes)
    required_bits = HEADER_SIZE + data_len * 8
    capacity = capacity_in_bits(img)

    if required_bits > capacity:
        raise ValueError(f"Message too large. Capacity bits: {capacity}, required bits: {required_bits}")

    header_bits = _int_to_bits(data_len, HEADER_SIZE)
    message_bits = list(_bytes_to_bits(data_bytes))
    bits = header_bits + message_bits

    pixels = list(img.getdata())
    new_pixels = []
    bit_idx = 0

    for r, g, b in pixels:
        if bit_idx < len(bits):
            r = (r & ~1) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | bits[bit_idx]
            bit_idx += 1

        new_pixels.append((r, g, b))

    out_img = Image.new('RGB', img.size)
    out_img.putdata(new_pixels)
    out_img.save(out_path, 'PNG')
    return out_path

def decode_bytes_from_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    bits = []

    for r, g, b in pixels:
        bits.extend([r & 1, g & 1, b & 1])

    header_bits = bits[:HEADER_SIZE]
    msg_len = 0
    for bit in header_bits:
        msg_len = (msg_len << 1) | bit

    total_message_bits = msg_len * 8
    message_bits = bits[HEADER_SIZE:HEADER_SIZE + total_message_bits]

    if len(message_bits) < total_message_bits:
        raise ValueError("Image does not contain a full message or header is corrupted.")

    return _bits_to_bytes(message_bits)