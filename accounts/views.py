from adrf.views import APIView as AsyncAPIView
from accounts.custom_authentication import IsAuthenticatedCustom
from accounts.models import Notification, User, Jwt
from accounts.notifications import user_notification
from accounts.responses import CustomSuccessResponse, CustomErrorResponse
from rest_framework.views import APIView
from accounts.serializers import LoginSerializer
from accounts.custom_functions import get_access_token, get_refresh_token
from django.contrib.auth import authenticate

class TriggerNotification(AsyncAPIView):
    permission_classes = [IsAuthenticatedCustom]
    async def get(self, request, *args, **kwargs):
        await Notification.objects.acreate(user = request.user,message= "a new notification has been triggered" )
        await user_notification(request.user, {"notification_type": "trigger", 
                                                "notification":"new notification triggered"
                                                })
        return CustomSuccessResponse({'message': 'a new notification has been triggered'})

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user =  User.objects.filter(email =  serializer.validated_data["email"])

      
        user = authenticate(request, email = serializer.validated_data["email"], password = serializer.validated_data["password"])

        if user is None:
            return CustomErrorResponse({"message":"Invalid details!"}, status=400)
        
        access = get_access_token({"user_id": str(user.id)})
        refresh = get_refresh_token()

        Jwt.objects.create(user = user, access = access, refresh = refresh)
        return CustomSuccessResponse({"access":access, "refresh":refresh})
    