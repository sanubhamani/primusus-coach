from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from qa_engine import get_response

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(request: Request):
    try:
        data = await request.json()
        message_body = data.get("Body", "")
        if not message_body:
            return JSONResponse(content={"reply": "No message received."}, status_code=400)
        
        reply = get_response(message_body)
        return {"reply": reply}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
