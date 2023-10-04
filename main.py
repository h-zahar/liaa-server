from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.service import generate_report, generate_text, generate_text_wh

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "https://liaa.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello, Hit": "https://localhost:5000/report?input=[conversation]"}


@app.get("/report")
async def get_generate_report(input: str):
    content = generate_report(input)
    if content['status'] == False:
        raise HTTPException(status_code=404, detail=content['msg'])
    return {'status_code': 200, 'content': content['msg']}


@app.get("/convert")
async def get_generate_text():

    content = generate_text()

    return {'status_code': 200, 'content': content}


@app.get("/convert-wh")
async def get_generate_text():

    content = generate_text_wh()

    return {'status_code': 200, 'content': content}
