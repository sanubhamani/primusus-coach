from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(Body: str = Form(...), From: str = Form(...)):
    print(f"Received message: {Body} from {From}")

    twilio_response = MessagingResponse()
    twilio_response.message(f"Got it: '{Body}' — we’ll coach you soon.")

    return Response(content=str(twilio_response), media_type="application/xml")
