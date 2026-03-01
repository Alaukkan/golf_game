

import socket
import threading
import json



class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        from typing import Optional

        self.sock: Optional[socket.socket] = None
        self.client_conn: Optional[socket.socket] = None
        self.client_addr = None
        self.running = False
        # internal buffer used by _recv_message
        self._recv_buffer = b""
        # event to signal when a client connects
        self._client_connected = threading.Event()

    def start(self):
        """Bind, listen and start accepting connections in a background thread."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow quick restart
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)  # only one client expected for 1v1
        self.running = True
        print(f"Listening on {self.host}:{self.port}")
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while self.running:
            try:
                conn, addr = self.sock.accept()
            except OSError:
                break
            print(f"Accepted connection from {addr}")
            # make client socket nonblocking for reads so the main thread can
            # poll without blocking
            conn.setblocking(False)
            self.client_conn = conn
            self.client_addr = addr
            self._client_connected.set()  # signal that client has connected

    def _recv_message(self, conn: socket.socket):
        """Read a JSON object terminated by newline from the socket.

        Because the socket is nonblocking we return ``None`` if there's no data
        available.  The caller must handle this by skipping updates rather than
        treating ``None`` as a complete packet.
        """
        if not self.client_conn:
            raise RuntimeError("No client connected")
        try:
            chunk = conn.recv(4096)
        except BlockingIOError:
            return None
        if not chunk:
            # empty bytes indicate the connection has been closed
            raise ConnectionResetError
        self._recv_buffer += chunk
        if b"\n" in self._recv_buffer:
            line, self._recv_buffer = self._recv_buffer.split(b"\n", 1)
            try:
                return json.loads(line.decode())
            except json.JSONDecodeError:
                return None
        return None

    def _send_message(self, conn: socket.socket, data):
        payload = json.dumps(data).encode() + b"\n"
        try:
            conn.sendall(payload)
        except BlockingIOError:
            # send buffer is full; data will be dropped this frame.
            # this is preferable to blocking the whole game loop.
            pass

    def send_game_data(self, data):
        """Send a JSON-serializable object to the connected client."""
        if not self.client_conn:
            raise RuntimeError("No client connected")
        print(f"Sending data to client: {data}\n")
        self._send_message(self.client_conn, data)

    def receive_game_data(self):
        """Nonblocking wrapper for ``_recv_message`` that returns ``None`` if no
        packet is waiting."""
        msg = self._recv_message(self.client_conn)
        if msg is not None:
            print(f"Receiving data from client: {msg}\n")
        return msg

    def wait_for_client(self, timeout = 30) -> bool:
        """Block until a client connects.  Returns True if client connected, False on timeout."""
        return self._client_connected.wait(timeout=timeout)

    def stop(self):
        """Shut down the server and close any connections."""
        self.running = False
        if self.client_conn:
            self.client_conn.close()
        if self.sock:
            self.sock.close()
