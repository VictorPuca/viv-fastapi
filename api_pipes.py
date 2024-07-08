# -*- encoding: utf-8 -*-

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from calc_pipe import calc_pipe
from soil_stiffness import soil_stiffness

app = FastAPI()

@app.post("/api")
async def main(request: Request):
    resp = await request.json()
    results = calc_pipe(**resp)
    return JSONResponse(content=results) #transformando respotas em jsonfile

@app.post("/api/soil_stiffness")
async def main2(request: Request):
    resp = await request.json()
    results = soil_stiffness(**resp)
    return JSONResponse(content=results) #transformando respotas em jsonfile

@app.middleware("http")
async def add_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)