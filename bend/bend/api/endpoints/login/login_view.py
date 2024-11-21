from rest_framework_simplejwt.views import TokenObtainPairView

from api.endpoints.login.login_serializer import LoginSerializer


class ApiLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
