from rest_framework import routers
from .views.clusters import ClusterViewSet
from .views.dbs import DBTypeViewSet
from .views.repositories import RepositoryViewSet


router = routers.SimpleRouter()
router.register(r'clusters', ClusterViewSet)
router.register(r'dbs', DBTypeViewSet)
router.register(r'repositories', RepositoryViewSet)
urlpatterns = router.urls
