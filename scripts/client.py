

import socket
import json


class Client:
    def __init__(self, server_host: str, server_port: int):
        self.server_host = server_host
        self.server_port = server_port
        from typing import Optional

        self.sock: Optional[socket.socket] = None
        self._recv_buffer = b""

    def connect(self, timeout: float | None = None):
        """Connect to the TCP server.  A timeout may be specified.

        After connecting we switch the socket to nonblocking mode so that
        ``receive_game_data`` can be called every frame without freezing the
        game loop.
        """
        print(f"Connecting to server at {self.server_host}:{self.server_port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # use a default 5-second timeout for initial connect so we don't hang forever
        # if the server isn't reachable
        if timeout is None:
            timeout = 5.0
        self.sock.settimeout(timeout)
        self.sock.connect((self.server_host, self.server_port))
        # switch to nonblocking mode for both reads and sends
        self.sock.setblocking(False)

    def _send_message(self, data):
        if not self.sock:
            raise RuntimeError("Not connected to server")
        payload = json.dumps(data).encode() + b"\n"
        try:
            # use send() instead of sendall() to avoid blocking the main thread.
            # send() returns as soon as the OS buffer accepts data, whereas
            # sendall() blocks until all data is sent.
            self.sock.send(payload)
        except BlockingIOError:
            # send buffer is full; data will be dropped this frame.
            # this is preferable to blocking the whole game loop.
            pass

    def _recv_message(self):
        if not self.sock:
            raise RuntimeError("Not connected to server")
        # nonblocking socket - may raise BlockingIOError when no data available
        try:
            chunk = self.sock.recv(4096)
        except BlockingIOError:
            # nothing to read right now
            return None
        if not chunk:
            # connection closed by server
            raise ConnectionResetError
        self._recv_buffer += chunk
        if b"\n" in self._recv_buffer:
            line, self._recv_buffer = self._recv_buffer.split(b"\n", 1)
            try:
                return json.loads(line.decode())
            except json.JSONDecodeError:
                return None
        return None

    def send_game_data(self, data):
        print(f"Sending data to server: {data}\n")
        self._send_message(data)

    def receive_game_data(self):
        msg = self._recv_message()
        if msg is not None:
            print(f"Receiving data from server: {msg}\n")
        return msg

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
    
