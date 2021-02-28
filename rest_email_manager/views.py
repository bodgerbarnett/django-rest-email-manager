from rest_framework import viewsets

from .models import EmailAddress
from .serializers import EmailAddressSerializer, CreateEmailAddressSerializer


class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEmailAddressSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
