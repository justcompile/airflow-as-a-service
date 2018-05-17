from rest_framework import routers
from .views.clusters import ClusterViewSet
from .views.dbs import DBTypeViewSet


router = routers.SimpleRouter()
router.register(r'clusters', ClusterViewSet)
router.register(r'dbs', DBTypeViewSet)
urlpatterns = router.urls
