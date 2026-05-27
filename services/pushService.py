import asyncio
import firebase_admin
from firebase_admin import credentials, messaging

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)


async def send_push(token: str, title: str, body: str):
    if not token:
        return

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    try:
        await asyncio.to_thread(messaging.send, message)
    except Exception as e:
        print(f"[Push Error] {e}")