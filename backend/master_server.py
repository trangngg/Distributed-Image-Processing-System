import socket
import threading
import os
from io import BytesIO
from typing import List
from PIL import Image

from image_util import split_image, reconstruct_image, convert_chunk

# Configuration from environment
HOST = os.environ.get("MASTER_HOST", "0.0.0.0")
MASTER_PORT = int(os.environ.get("MASTER_PORT", 5003))
NUM_WORKERS = int(os.environ.get("NUM_WORKERS", 4))


def recv_bytes(conn: socket.socket) -> bytes:
    """Receive a byte sequence via socket with 4-byte length prefix"""
    raw_len = conn.recv(4)
    if not raw_len:
        return b""
    length = int.from_bytes(raw_len, byteorder="big")
    data = b""
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            break
        data += packet
    return data


def send_bytes(conn: socket.socket, data: bytes) -> None:
    """Send a byte sequence via socket with 4-byte length prefix"""
    length = len(data)
    conn.sendall(length.to_bytes(4, byteorder="big"))
    conn.sendall(data)


def bytes_to_image(data: bytes) -> Image.Image:
    """Convert raw bytes to a PIL Image"""
    return Image.open(BytesIO(data))


def handle_worker_connection(conn: socket.socket, addr: tuple):
    """
    Handle a single worker connection in a daemon thread.
    Receives raw segment bytes, processes it, and returns result bytes.
    """
    try:
        while True:
            chunk = recv_bytes(conn)
            if not chunk:
                break
            result = convert_chunk(chunk)
            send_bytes(conn, result)
    except Exception as e:
        print(f"Worker handler error from {addr}: {e}")
    finally:
        conn.close()


def process_image_distributed_bytes(img_bytes: bytes) -> bytes:
    """
    Distribute image processing across workers via master-server:
    1) Convert bytes→Image
    2) Split image into segments
    3) Send each segment to master-server; collect processed segments
    4) Reconstruct full grayscale image and return bytes
    """
    # 1) Bytes to PIL Image
    img = bytes_to_image(img_bytes)

    # 2) Split into segments
    segments = split_image(img, NUM_WORKERS)

    gray_segments: List[bytes] = []
    # 3) Exchange segments with master-server
    for seg_bytes in segments:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, MASTER_PORT))
            send_bytes(s, seg_bytes)
            processed = recv_bytes(s)
            gray_segments.append(processed)

    # 4) Reconstruct full image
    result_bytes = reconstruct_image(gray_segments)
    return result_bytes


def start_master_server():
    """
    Launch master-server listening for worker connections.
    Spawns a daemon thread per connection.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, MASTER_PORT))
    s.listen()
    print(f"Master-server listening on {HOST}:{MASTER_PORT}")

    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_worker_connection,
                args=(conn, addr),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("Shutting down master-server…")
    finally:
        s.close()


if __name__ == "__main__":
    start_master_server()
