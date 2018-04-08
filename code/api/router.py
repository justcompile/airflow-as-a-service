from rest_framework import routers
from .views.clusters import ClusterViewSet

router = routers.SimpleRouter()
router.register(r'clusters', ClusterViewSet)
urlpatterns = router.urls
