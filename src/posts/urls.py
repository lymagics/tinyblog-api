from rest_framework.routers import DefaultRouter

from .api.views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
urlpatterns = router.urls

app_name = 'posts'
