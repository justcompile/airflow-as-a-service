from rest_framework import routers

from payments.api.router import urlpatterns as payment_urls

from .views.builds import BuildViewSet
from .views.clusters import ClusterViewSet
from .views.dbs import DBTypeViewSet
from .views.repositories import RepositoryViewSet


router = routers.SimpleRouter()
router.register(r'builds', BuildViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'dbs', DBTypeViewSet)
router.register(r'repositories', RepositoryViewSet)

urlpatterns = router.urls + payment_urls
