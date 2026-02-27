# golf_game

**WORK IN PROGRESS**

Golf game similar to Nintendo's NES Open golf game from the 90's.

## Networking (1‑vs‑1 online)

A simple TCP-based protocol is used for turn‑based multiplayer.  The
`scripts/server.py` and `scripts/client.py` classes wrap the standard
`socket` module and serialize each message as JSON terminated by a newline.

Basic usage:

```python
# server side
from scripts.server import Server

srv = Server('0.0.0.0', 9999)
srv.start()
# ... later when a client has connected:

srv.send_game_data({'type': 'stroke', 'x': 10, 'y': 20})
data = srv.receive_game_data()
```

```python
# client side
from scripts.client import Client

cli = Client('server.address', 9999)
cli.connect()
cli.send_game_data({'type': 'ready'})
resp = cli.receive_game_data()
```

The connection is reliable and in‑order thanks to TCP, which is sufficient
for a turn‑based game.  You can stop the server with `srv.stop()` and close
the client with `cli.close()`.
```
