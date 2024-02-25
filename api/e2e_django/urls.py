from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from demo.views import ItemViewSet

router = routers.SimpleRouter()
router.register("items", ItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
