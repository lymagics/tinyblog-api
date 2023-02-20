from django.urls import path

from rest_framework.routers import DefaultRouter

from .api.views import UserViewSet, MeAPIView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('me/', MeAPIView.as_view(), name='me'),
]
urlpatterns += router.urls

app_name = 'users'
