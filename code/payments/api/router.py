from django.conf.urls import url
from rest_framework import routers
from .views import PlanViewSet, SubscribeView


router = routers.SimpleRouter()
router.register(r'plans', PlanViewSet)
urlpatterns = router.urls
urlpatterns += [url(r'subscribe', SubscribeView.as_view())]
