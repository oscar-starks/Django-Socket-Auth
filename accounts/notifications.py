import json, websockets
from accounts.custom_functions import get_access_token
from decouple import config
HOST = config("HOST")

async def user_notification(receiver, data):
    notification_data = {
        "notification_type": data.pop("notification_type"),
        "notification_data": data
        }
    
    access = get_access_token({"user_id": (str(receiver.id))})
    uri = f"ws://{HOST}/ws/notification/"
   
    async with websockets.connect(uri, extra_headers={"token":access}) as websocket:
        await websocket.send(json.dumps({"data":notification_data}))
