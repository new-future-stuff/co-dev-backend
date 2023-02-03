from rest_framework import permissions, viewsets, mixins

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_class = [permissions.IsAuthenticated]
