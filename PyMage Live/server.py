import asyncio
import os
import pty
import fcntl
import termios
import struct
import signal
from aiohttp import web, WSMsgType

GAME_CMD = ["python", "PyMage (v1.1).py"]
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


async def index(request):
    raise web.HTTPFound("/static/index.html")


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Open a PTY and spawn the game
    master_fd, slave_fd = pty.openpty()

    # Set a reasonable terminal size
    winsize = struct.pack("HHHH", 24, 80, 0, 0)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)

    loop = asyncio.get_event_loop()
    process = await asyncio.create_subprocess_exec(
        *GAME_CMD,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        preexec_fn=os.setsid,
    )
    os.close(slave_fd)

    # Make master_fd non-blocking
    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    stop = asyncio.Event()

    async def pty_to_ws():
        """Read PTY output and send to browser."""
        while not stop.is_set():
            try:
                await asyncio.sleep(0.01)
                try:
                    data = os.read(master_fd, 4096)
                except BlockingIOError:
                    continue
                except OSError:
                    break
                if data:
                    await ws.send_bytes(data)
            except Exception:
                break
        stop.set()

    async def ws_to_pty():
        """Read browser input and write to PTY."""
        async for msg in ws:
            if msg.type == WSMsgType.BINARY:
                try:
                    os.write(master_fd, msg.data)
                except OSError:
                    break
            elif msg.type == WSMsgType.TEXT:
                data = msg.data
                # Handle terminal resize: "resize:rows:cols"
                if data.startswith("resize:"):
                    parts = data.split(":")
                    if len(parts) == 3:
                        try:
                            rows = int(parts[1])
                            cols = int(parts[2])
                            winsize = struct.pack("HHHH", rows, cols, 0, 0)
                            fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)
                        except Exception:
                            pass
                else:
                    try:
                        os.write(master_fd, data.encode())
                    except OSError:
                        break
            elif msg.type in (WSMsgType.ERROR, WSMsgType.CLOSE):
                break
        stop.set()

    reader_task = asyncio.ensure_future(pty_to_ws())
    writer_task = asyncio.ensure_future(ws_to_pty())

    await stop.wait()

    reader_task.cancel()
    writer_task.cancel()

    # Clean up
    try:
        process.send_signal(signal.SIGTERM)
    except Exception:
        pass
    try:
        os.close(master_fd)
    except Exception:
        pass
    try:
        await asyncio.wait_for(process.wait(), timeout=3)
    except Exception:
        try:
            process.kill()
        except Exception:
            pass

    return ws


def make_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)
    app.router.add_static("/static", STATIC_DIR)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = make_app()
    web.run_app(app, host="0.0.0.0", port=port)
