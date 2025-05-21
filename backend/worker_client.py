# worker_client.py

import socket
import os
import time
from network import send_bytes, recv_bytes
from image_util import image_to_bytes, bytes_to_image

# Đọc host/port từ environment, default trùng với cài đặt trong Docker
MASTER_HOST = os.environ.get("MASTER_HOST", "127.0.0.1")
MASTER_PORT = int(os.environ.get("MASTER_PORT", "5003"))

def main():
    while True:
        try:
            # Kết nối về Master-Server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((MASTER_HOST, MASTER_PORT))
                # Nhận segment
                data = recv_bytes(s)
                # Chuyển PIL image sang gray
                img = bytes_to_image(data).convert('L')
                out = image_to_bytes(img)
                # Gửi lại kết quả
                send_bytes(s, out)
        except ConnectionRefusedError:
            # Master chưa sẵn sàng → chờ rồi thử lại
            time.sleep(1)
        except Exception as e:
            print("Worker error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
