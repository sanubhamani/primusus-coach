from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(request: Request):
    data = await request.json()
    body = data.get("Body", "")
    sender = data.get("From", "")
    print(f"Received message: {body} from {sender}")
    return JSONResponse(content={"reply": f"Got it: '{body}' — we’ll coach you soon."})

