from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('tokens/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('tokens/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

app_name = 'tokens'
