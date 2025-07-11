from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.post("/whatsapp-hook")
async def whatsapp_hook(request: Request):
    data = await request.form()
    body = data.get("Body", "")
    sender = data.get("From", "")
    print(f"Received message: {body} from {sender}")

    # Build Twilio XML reply
    response = MessagingResponse()
    response.message(f"Got it: '{body}' — we’ll coach you soon.")

    return Response(content=str(response), media_type="application/xml")
