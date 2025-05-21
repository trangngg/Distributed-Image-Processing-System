import socket
import io

def send_bytes(conn: socket.socket, data: bytes) -> None:
    """
    Gửi data đã cho qua socket kèm header 8 byte biểu diễn độ dài dữ liệu.
    """
    length = len(data)
    conn.sendall(length.to_bytes(8, 'big'))
    conn.sendall(data)

def _recvall(conn: socket.socket, n: int) -> bytes:
    """
    Đọc chính xác n byte từ socket.
    """
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed while receiving")
        buf += chunk
    return buf

def recv_bytes(conn: socket.socket) -> bytes:
    """
    Nhận dữ liệu được gửi kèm header 8 byte độ dài.
    """
    length_bytes = _recvall(conn, 8)
    length = int.from_bytes(length_bytes, 'big')
    return _recvall(conn, length)
