from rest_framework.serializers import ModelSerializer

from ..models import Post
from users.api.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    """
    DRF serializer to represent Post model.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'timestamp', 'author',)
        read_only_fields = ('id', 'timestamp', 'author',)
