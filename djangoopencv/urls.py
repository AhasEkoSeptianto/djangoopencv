from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from face_detector import views as viewsFaceDetect

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('detect', views.DetectImage),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('face_detection/detect', viewsFaceDetect.detect)
]
