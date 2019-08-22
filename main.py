import asyncio
from aiohttp import web
import tempfile

async def root_handler(request):
    return web.HTTPFound('/index.html')

async def run_code(request):
    with tempfile.NamedTemporaryFile() as code_file:
        with open(code_file.name, 'w') as fd:
            fd.write(await request.text())
        proc = await asyncio.create_subprocess_exec(
            'python3', code_file.name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
        except asyncio.TimeoutError:
            proc.kill()
            stdout, stderr = await proc.communicate()

    return web.json_response({
        'stdout': stdout.decode('utf-8'),
        'stderr': stderr.decode('utf-8'),
    })

app = web.Application()
app.add_routes([web.static('/', '/', show_index=True),
                web.post('/api/run', run_code)])
web.run_app(app, port=12385)
