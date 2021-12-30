import asyncio
from aiohttp import web, WSMsgType
import collections
import hashlib
import json
import os
import sys
import tempfile


def hash_directory(directory):
    hash_builder = hashlib.md5()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            hash_builder.update(filepath.encode("utf-8"))
            file_hash = hashlib.md5(open(filepath, "rb").read()).digest()
            hash_builder.update(file_hash)

    return hash_builder.hexdigest()


def serve_file(path):
    async def fn(_):
        return web.FileResponse(path)

    return fn


class AlephZeroLibraryBuilder:
    dir_hashes = collections.defaultdict(str)

    @staticmethod
    async def rebuild():
        cpp_hash = hash_directory("/alephzero/alephzero")

        if cpp_hash != AlephZeroLibraryBuilder.dir_hashes["cpp_code"]:
            print("Rebuilding C++ Code...", file=sys.stderr)
            proc = await asyncio.create_subprocess_exec(
                "make",
                "-j",
                "install",
                cwd="/alephzero/alephzero",
                env=dict(os.environ, A0_EXT_NLOHMANN="1", A0_EXT_YYJSON="1"),
            )
            await proc.wait()
            AlephZeroLibraryBuilder.dir_hashes["cpp_code"] = cpp_hash

        py_hash = hash_directory("/alephzero/py")

        if py_hash != AlephZeroLibraryBuilder.dir_hashes["py_code"]:
            print("Rebuilding Python Code...", file=sys.stderr)
            proc = await asyncio.create_subprocess_exec(
                "python3", "-m", "pip", "install", ".", cwd="/alephzero/py"
            )
            await proc.wait()
            AlephZeroLibraryBuilder.dir_hashes["py_code"] = py_hash


class CodeRunner:
    def __init__(self, cmd, ws_out):
        self.cmd = cmd
        self.ws_out = ws_out
        self.proc = None
        self.dead = False

    async def run(self):
        if self.dead:
            return

        code_file = tempfile.NamedTemporaryFile(
            suffix="." + self.cmd["lang"], delete=False
        )
        with open(code_file.name, "w") as fd:
            fd.write(self.cmd["code"])

        await AlephZeroLibraryBuilder.rebuild()

        if self.cmd["lang"] == "py":
            self.proc = await asyncio.create_subprocess_exec(
                "python3",
                "-u",
                code_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        elif self.cmd["lang"] == "cpp":
            bin_file = tempfile.NamedTemporaryFile(delete=False)
            self.proc = await asyncio.create_subprocess_exec(
                "g++",
                "-std=c++17",
                "-o",
                bin_file.name,
                "-DA0_EXT_NLOHMANN",
                "-I/alephzero/alephzero/third_party/json/single_include",
                "-DA0_EXT_YYJSON",
                "-I/alephzero/alephzero/third_party/yyjson/src",
                code_file.name,
                "-lalephzero",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            build_result = await self.proc.wait()
            if build_result:
                await self.ws_out.send_json(
                    {
                        "stream": "stderr",
                        "output": (await self.proc.stderr.read()).decode("utf-8"),
                    }
                )
                return
            bin_file.close()
            self.proc = await asyncio.create_subprocess_exec(
                bin_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            await self.ws_out.send_json(
                {
                    "stream": "stderr",
                    "output": "Error: Unknown language!",
                }
            )
            return
        if self.dead:
            await self.kill()
            return
        asyncio.ensure_future(self._stream(self.proc.stdout, "stdout"))
        asyncio.ensure_future(self._stream(self.proc.stderr, "stderr"))
        await self.proc.wait()

    async def kill(self):
        self.dead = True
        self.ws_out = None
        if self.proc:
            try:
                self.proc.kill()
            except Exception:
                pass

    async def _stream(self, stream, name):
        while True:
            line = await stream.read(1024)
            if not self.dead and line:
                await self.ws_out.send_json(
                    {
                        "stream": name,
                        "output": line.decode("utf-8"),
                    }
                )
            else:
                break


async def run_code_handshake(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    class State:
        runner = None

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == "close":
                await State.runner.kill()
            else:
                State.runner = CodeRunner(json.loads(msg.data), ws)
                asyncio.ensure_future(State.runner.run())
        elif msg.type == WSMsgType.ERROR:
            if State.runner:
                await State.runner.kill()
            break
    if State.runner:
        await State.runner.kill()


asyncio.get_event_loop().run_until_complete(AlephZeroLibraryBuilder.rebuild())

app = web.Application()
app.add_routes(
    [
        web.get("/", serve_file("/index.html")),
        web.get("/examples.json", serve_file("/examples.json")),
        web.static("/examples", "/examples"),
        web.get("/api/run", run_code_handshake),
    ]
)
web.run_app(app, port=12385)
