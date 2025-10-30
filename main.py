from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Attachment(BaseModel):
    url: str

class InputData(BaseModel):
    attachments: Attachment

@app.post("/file")
async def detect_mime_type(data: InputData):
    data_uri = data.attachments.url
    match = re.match(r'data:(.*?);base64,', data_uri)
    if match:
        mime_type = match.group(1)
        if mime_type.startswith('image/'):
            return {"type": "image"}
        elif mime_type.startswith('text/'):
            return {"type": "text"}
        elif mime_type.startswith('application/'):
            return {"type": "application"}
        else:
            return {"type": "unknown"}
    else:
        return {"type": "unknown"}
