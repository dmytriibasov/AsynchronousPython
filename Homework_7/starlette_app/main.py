from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def index(request):
    return PlainTextResponse('Hello World!')

routes = [
    Route('/', index)
]

app = Starlette(debug=True, routes=routes)
