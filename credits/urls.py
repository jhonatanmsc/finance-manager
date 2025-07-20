from rest_framework import routers

from credits.views import CreditViewSet

router = routers.DefaultRouter()
router.register(r"credits", CreditViewSet)
