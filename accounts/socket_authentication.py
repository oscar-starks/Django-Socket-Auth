import json, jwt
from channels.auth import AuthMiddlewareStack
from asgiref.sync import sync_to_async
from django.conf import settings
from accounts.socket_serializer import serialize_json
from accounts.models import User

def decodeJWTForSocket(bearer):
    if not bearer:
        return None
    
    try:
        decoded = jwt.decode(bearer, settings.SECRET_KEY, algorithms=["HS256"])
    except:
        return None

    if decoded:
        try:
            user = User.objects.get(id=decoded["user_id"])
            return user
        except Exception:
            return None


async def authenticate(self, callback = None):
    '''
        this takes the default argument of self and an optional callback. the callback 
        is a function that will be called if you want to perform the authentication
        yourself.
    '''
    self.user = self.scope["user"]

    if self.user is not None:
        id = await sync_to_async(getattr)(self.user, "id")
        self.room_group_name = f"{id}__notifications"

        if callback is not None:
            response = await callback(self)
        
            await self.send(text_data=json.dumps({
            'type': response["status"],
            'message': response["message"]})
            )

            if not response["connection_status"]:
                await self.close(code=1000)

        else:
            await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)

            await self.accept()

            await self.send(text_data=json.dumps({
                'type': 'connection established',
                'message': 'connection successful'})
                )
    else:
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection rejected',
            'message': 'authentication failed'})
        )
        await self.close(code=1000)



class TokenAuthMiddleware:
    '''
        this middleware populates the scope['user'] with the credentials of the authenticated user
        when the authentication is successful else scop['user'] will be None
    '''
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers_dict = {key.decode(): value.decode() for key, value in scope["headers"]}

        try:
            query_string = scope['query_string']
            query_string = str(query_string)

            if 'token' in headers_dict:
                token = headers_dict["token"]
                user = await sync_to_async(decodeJWTForSocket)(token)

                if not user:
                    scope["user"] = None
                else:
                    scope["user"] = user

        except:
            scope["user"] = None
            

        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
