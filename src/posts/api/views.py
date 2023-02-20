from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import PostSerializer
from ..models import Post
from ..permissions import IsOwnerOrReadOnly
from core.mixins import PartialUpdateMixin


class PostViewSet(PartialUpdateMixin, ModelViewSet):
    """
    Posts endpoint.
    """

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Post.objects.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
