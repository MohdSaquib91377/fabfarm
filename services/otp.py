from django.conf import settings
from twilio.rest import Client

def send_twilio_sms(msg_to: str, msg_otp: str) -> None:
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Login OTP {msg_otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=f"+91{msg_to}",
    )
    