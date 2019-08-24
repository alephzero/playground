import asyncio
from aiohttp import web, WSMsgType, __version__
import json
import tempfile

print('aiohttp.__version__', __version__)

class Namespace:
    pass

async def root_handler(request):
    return web.FileResponse('/index.html')

class CodeRunner:
    def __init__(self, cmd, ws_out):
        self.cmd = cmd
        self.ws_out = ws_out
        self.proc = None
        self.dead = False

    async def run(self):
        if self.dead:
            return
        self.code_file = tempfile.NamedTemporaryFile()
        with open(self.code_file.name, 'w') as fd:
            fd.write(self.cmd['code'])
        # self.cmd['lang']
        self.proc = await asyncio.create_subprocess_exec(
            'python3', '-u', self.code_file.name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        if self.dead:
            await self.kill()
            return
        asyncio.ensure_future(self._stream(self.proc.stdout, 'stdout'))
        asyncio.ensure_future(self._stream(self.proc.stderr, 'stderr'))
        await self.proc.wait()

    async def kill(self):
        self.dead = True
        self.ws_out = None
        if self.proc:
            try:
                self.proc.kill()
            except:
                pass

    async def _stream(self, stream, name):
        while True:
            line = await stream.read(1024)
            if not self.dead and line:
                await self.ws_out.send_json({
                    'stream': name,
                    'output': line.decode('utf-8'),
                })
            else:
                break

async def run_code_handshake(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    ns = Namespace()
    ns.runner = None
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ns.runner.kill()
            else:
                ns.runner = CodeRunner(json.loads(msg.data), ws)
                asyncio.ensure_future(ns.runner.run())
        elif msg.type == WSMsgType.ERROR:
            if ns.runner:
                await ns.runner.kill()
            break
    if ns.runner:
        await ns.runner.kill()

app = web.Application()
app.add_routes([web.get('/', root_handler),
                web.get('/api/run', run_code_handshake)])
web.run_app(app, port=12385)
