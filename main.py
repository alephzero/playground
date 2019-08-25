import asyncio
from aiohttp import web, WSMsgType
import json
import tempfile

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

        code_file = tempfile.NamedTemporaryFile(suffix='.' + self.cmd['lang'], delete=False)
        with open(code_file.name, 'w') as fd:
            fd.write(self.cmd['code'])

        if self.cmd['lang'] == 'py':
            self.proc = await asyncio.create_subprocess_exec(
                'python3', '-u', code_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        elif self.cmd['lang'] == 'go':
            self.proc = await asyncio.create_subprocess_exec(
                'go', 'run', code_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        elif self.cmd['lang'] == 'cc':
            bin_file = tempfile.NamedTemporaryFile(delete=False)
            self.proc = await asyncio.create_subprocess_exec(
                'g++', '-o', bin_file.name, code_file.name, '-lalephzero',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            build_result = await self.proc.wait()
            if build_result:
                await self.ws_out.send_json({
                    'stream': 'stderr',
                    'output': (await self.proc.stderr.read()).decode('utf-8'),
                })
                return
            bin_file.close()
            self.proc = await asyncio.create_subprocess_exec(
                bin_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        else:
            await self.ws_out.send_json({
                'stream': 'stderr',
                'output': 'Error: Unknown language!',
            })
            return
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
