import asyncio
from aiohttp import web, WSMsgType
import json
import tempfile

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __getattr__(self, name):
        return self.__dict__.get(name, None)

global_ns = Namespace()

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

        proc = await asyncio.create_subprocess_exec(
            'make', '-j', 'install',
            cwd='/alephzero/alephzero')
        await proc.wait()

        if self.cmd['lang'] == 'py':
            py_requirements = open('/alephzero/py/requirements.txt', 'rb').read()
            if global_ns.py_requirements != py_requirements:
                # TODO: Forward stderr.
                proc = await asyncio.create_subprocess_exec(
                    'pip3', 'install', '-r', 'requirements.txt',
                    cwd='/alephzero/py')
                await proc.wait()
            global_ns.py_requirements = py_requirements

            proc = await asyncio.create_subprocess_exec(
                'python3', 'setup.py', 'install',
                cwd='/alephzero/py')
            await proc.wait()

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
                'g++', '-std=c++17', '-D_GLIBCXX_USE_CXX11_ABI=0', '-o', bin_file.name, code_file.name, '-lalephzero',
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
                web.static('/examples', '/examples'),
                web.get('/api/run', run_code_handshake)])
web.run_app(app, port=12385)
