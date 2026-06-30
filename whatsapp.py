import requests

ACCESS_TOKEN = "YOUR_NEW_ACCESS_TOKEN"
PHONE_NUMBER_ID = "1214825448377822"

URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


def send_owner_notification(message, phone):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(URL, headers=headers, json=data)

    print(response.status_code)
    print(response.text)