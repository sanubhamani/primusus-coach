from fastapi import FastAPI, Request
from qa_engine import get_response

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(request: Request):
    data = await request.json()
    user_input = data.get("Body", "")
    reply = get_response(user_input)
    return {"reply": reply}
