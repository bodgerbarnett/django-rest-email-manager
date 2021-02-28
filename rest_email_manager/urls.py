from rest_framework import routers

from .views import EmailAddressViewSet


router = routers.DefaultRouter()
router.register('', EmailAddressViewSet)


urlpatterns = router.urls
