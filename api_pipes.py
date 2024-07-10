# -*- encoding: utf-8 -*-

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from calc_pipe import calc_pipe
from soil_stiffness import soil_stiffness
from typing import List, Dict, Any
import json

app = FastAPI()

# Carrega os dados do arquivo JSON
with open("db.json", "r") as file:
    pipes = json.load(file)["pipes"]

@app.get("/pipes", response_model=List[Dict[str, Any]])
def get_pipes():
    return pipes

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