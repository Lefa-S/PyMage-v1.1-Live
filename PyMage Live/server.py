import asyncio
import os
import pty
import fcntl
import termios
import struct
import signal
from aiohttp import web, WSMsgType

GAME_CMD = ["python", "PyMage (v1.1).py"]

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PyMage 🧙</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.min.css" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0d0d1a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: 'Segoe UI', system-ui, sans-serif;
      color: #e0e0ff;
    }
    header { text-align: center; margin-bottom: 20px; }
    header h1 {
      font-size: 2rem;
      letter-spacing: 0.1em;
      color: #a78bfa;
      text-shadow: 0 0 20px #7c3aed88;
    }
    header p { font-size: 0.9rem; color: #6b7280; margin-top: 4px; }
    #terminal-wrapper {
      border: 1px solid #2e2e4d;
      border-radius: 10px;
      padding: 12px;
      background: #0a0a14;
      box-shadow: 0 0 40px #7c3aed33, 0 8px 32px #00000088;
      width: min(900px, 96vw);
    }
    #terminal-bar {
      display: flex;
      align-items: center;
      gap: 6px;
      padding-bottom: 10px;
      border-bottom: 1px solid #1e1e3a;
      margin-bottom: 10px;
    }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red    { background: #ff5f57; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green  { background: #28c840; }
    #terminal-title {
      flex: 1;
      text-align: center;
      font-size: 0.8rem;
      color: #4b5563;
      letter-spacing: 0.05em;
    }
    #terminal { width: 100%; }
    #status {
      margin-top: 14px;
      text-align: center;
      font-size: 0.8rem;
      color: #4b5563;
      min-height: 1.2em;
    }
    #status.connected { color: #34d399; }
    #status.error     { color: #f87171; }
    footer { margin-top: 24px; font-size: 0.75rem; color: #374151; }
  </style>
</head>
<body>
  <header>
    <h1>🧙 PyMage</h1>
    <p>A mage battle in the terminal — fight the AI with spells and strategy.</p>
  </header>
  <div id="terminal-wrapper">
    <div id="terminal-bar">
      <span class="dot dot-red"></span>
      <span class="dot dot-yellow"></span>
      <span class="dot dot-green"></span>
      <span id="terminal-title">pymage — battle</span>
    </div>
    <div id="terminal"></div>
  </div>
  <div id="status">Connecting…</div>
  <footer>Created by Mojalefa Sekgobela · May 2025</footer>
  <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.min.js"></script>
  <script>
    const statusEl = document.getElementById('status');
    const term = new Terminal({
      cursorBlink: true,
      fontSize: 15,
      fontFamily: '"Cascadia Code", "Fira Code", "JetBrains Mono", monospace',
      theme: {
        background: '#0a0a14', foreground: '#e2e2ff', cursor: '#a78bfa',
        selectionBackground: '#7c3aed44',
        black: '#1e1e2e', brightBlack: '#45475a',
        red: '#f38ba8', brightRed: '#f38ba8',
        green: '#a6e3a1', brightGreen: '#a6e3a1',
        yellow: '#f9e2af', brightYellow: '#f9e2af',
        blue: '#89b4fa', brightBlue: '#89b4fa',
        magenta: '#cba6f7', brightMagenta: '#cba6f7',
        cyan: '#89dceb', brightCyan: '#89dceb',
        white: '#cdd6f4', brightWhite: '#cdd6f4',
      },
      convertEol: true,
      scrollback: 1000,
    });
    const fitAddon = new FitAddon.FitAddon();
    term.loadAddon(fitAddon);
    term.open(document.getElementById('terminal'));
    fitAddon.fit();

    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    const ws = new WebSocket(`${proto}://${location.host}/ws`);
    ws.binaryType = 'arraybuffer';

    ws.onopen = () => {
      statusEl.textContent = 'Connected — type your move below';
      statusEl.className = 'connected';
      sendResize();
    };
    ws.onclose = () => {
      statusEl.textContent = 'Session ended — refresh to play again';
      statusEl.className = 'error';
      term.write('\\r\\n\\r\\n\\x1b[33m[ Session ended. Refresh the page to play again. ]\\x1b[0m\\r\\n');
    };
    ws.onerror = () => { statusEl.textContent = 'Connection error'; statusEl.className = 'error'; };
    ws.onmessage = (e) => {
      if (e.data instanceof ArrayBuffer) term.write(new Uint8Array(e.data));
      else term.write(e.data);
    };
    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) ws.send(new TextEncoder().encode(data));
    });
    function sendResize() {
      if (ws.readyState === WebSocket.OPEN) ws.send(`resize:${term.rows}:${term.cols}`);
    }
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => { fitAddon.fit(); sendResize(); }, 100);
    });
    term.onResize(() => sendResize());
  </script>
</body>
</html>"""


async def index(request):
    return web.Response(text=HTML, content_type="text/html")


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    master_fd, slave_fd = pty.openpty()

    winsize = struct.pack("HHHH", 24, 80, 0, 0)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, winsize)

    process = await asyncio.create_subprocess_exec(
        *GAME_CMD,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        preexec_fn=os.setsid,
    )
    os.close(slave_fd)

    flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
    fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    stop = asyncio.Event()

    async def pty_to_ws():
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
        async for msg in ws:
            if msg.type == WSMsgType.BINARY:
                try:
                    os.write(master_fd, msg.data)
                except OSError:
                    break
            elif msg.type == WSMsgType.TEXT:
                data = msg.data
                if data.startswith("resize:"):
                    parts = data.split(":")
                    if len(parts) == 3:
                        try:
                            rows, cols = int(parts[1]), int(parts[2])
                            fcntl.ioctl(master_fd, termios.TIOCSWINSZ,
                                        struct.pack("HHHH", rows, cols, 0, 0))
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
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = make_app()
    web.run_app(app, host="0.0.0.0", port=port)
