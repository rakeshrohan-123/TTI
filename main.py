import io
from PIL import Image
import base64
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HEADERS = {"Authorization": "Bearer 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"}

def query_model(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        raise HTTPException(status_code=response.status_code, detail="Model query failed")

@app.post("/process_image/")
async def process_image(image_query: dict):
    if 'image_query' not in image_query:
        raise HTTPException(status_code=400, detail="image_query field is required")
    
    image_bytes = query_model({"inputs": image_query['image_query']})
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return {"image_base64": image_base64}
