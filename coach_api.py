from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from qa_engine import get_response  # NEW

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(Body: str = Form(...), From: str = Form(...)):
    print(f"Received message: {Body} from {From}")

    reply = get_response(Body)  # SMART REPLY from course content

    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return Response(content=str(twilio_response), media_type="application/xml")
