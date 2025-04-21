import requests
import africastalking
from twilio.rest import Client

class SMSManager:
    def __init__(self):
        # Twilio Credentials
        self.twilio_sid = "your_twilio_sid"
        self.twilio_auth_token = "your_twilio_auth_token"
        self.twilio_phone_number = "+123456789"

        # Nexmo (Vonage) Credentials
        self.nexmo_api_key = "your_nexmo_api_key"
        self.nexmo_api_secret = "your_nexmo_api_secret"

        # Africa's Talking Credentials
        self.africastalking_username = "your_username"
        self.africastalking_api_key = "your_api_key"
        africastalking.initialize(self.africastalking_username, self.africastalking_api_key)

        # FayaSMS Credentials
        self.fayasms_api_key = "your_fayasms_api_key"
        self.fayasms_sender_id = "your_sender_id"  # Set your approved sender ID

    def send_sms(self, phone_number, message, provider="twilio"):
        """
        Sends an SMS using the specified provider.
        
        :param phone_number: str - Customer's phone number (include country code).
        :param message: str - The SMS message to send.
        :param provider: str - The SMS API to use ('twilio', 'nexmo', 'africastalking', 'fayasms').
        :return: dict - Response data from the API.
        """

        if provider == "twilio":
            return self.send_via_twilio(phone_number, message)
        elif provider == "nexmo":
            return self.send_via_nexmo(phone_number, message)
        elif provider == "africastalking":
            return self.send_via_africastalking(phone_number, message)
        elif provider == "fayasms":
            return self.send_via_fayasms(phone_number, message)
        else:
            return {"error": "Invalid SMS provider"}

    def send_via_twilio(self, phone_number, message):
        """Send SMS using Twilio"""
        try:
            client = Client(self.twilio_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=phone_number
            )
            return {"status": "success", "message_id": message.sid}
        except Exception as e:
            return {"error": str(e)}

    def send_via_nexmo(self, phone_number, message):
        """Send SMS using Nexmo (Vonage)"""
        try:
            url = "https://rest.nexmo.com/sms/json"
            data = {
                "from": "YourBrand",
                "text": message,
                "to": phone_number,
                "api_key": self.nexmo_api_key,
                "api_secret": self.nexmo_api_secret
            }
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def send_via_africastalking(self, phone_number, message):
        """Send SMS using Africa's Talking"""
        try:
            sms = africastalking.SMS
            response = sms.send(message, [phone_number])
            return response
        except Exception as e:
            return {"error": str(e)}

    def send_via_fayasms(self, phone_number, message):
        """Send SMS using FayaSMS"""
        try:
            url = "https://fayasms.com/api/send"
            headers = {
                "Authorization": f"Bearer {self.fayasms_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "sender_id": self.fayasms_sender_id,
                "message": message,
                "recipient": phone_number
            }
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Example usage:
sms_manager = SMSManager()
response = sms_manager.send_sms("+254712345678", "Hello, this is a test message!", provider="fayasms")
print(response)
