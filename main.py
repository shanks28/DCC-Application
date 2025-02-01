from fastapi import FastAPI
from Router import blender_endpoints
app=FastAPI()
app.include_router(blender_endpoints.router,prefix="/object")
@app.get("/")
async def root():
    return "Hello World"