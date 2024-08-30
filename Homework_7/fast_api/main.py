from fastapi import FastAPI

from fast_api.schemas import Response

app = FastAPI()

@app.get("/", response_model=Response)
async def index() -> Response:
    return Response(message="Hello World!")
