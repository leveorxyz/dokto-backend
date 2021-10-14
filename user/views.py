from core.views import CustomRetrieveAPIView
from .models import User
from .serializers import UserSerializer


class UserRetrieveAPIView(CustomRetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
