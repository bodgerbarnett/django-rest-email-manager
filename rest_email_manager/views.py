from rest_framework import permissions, viewsets

from .models import EmailAddress
from .serializers import EmailAddressSerializer


class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.emailaddresses.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
