from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from .serializers import UserSerializer, UpdateUserSerializer
from ..models import User
from core.mixins import PartialUpdateMixin
from posts.api.serializers import PostSerializer


class UserViewSet(ModelViewSet):
    """
    Users endpoint.
    """

    http_method_names = ('get', 'post',)
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

    @action(
        methods=['get',],
        detail=True,
    )
    def posts(self, request, username):
        user = self.get_object()
        queryset = user.posts.all()

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        posts = PostSerializer(page, many=True)
        return paginator.get_paginated_response(posts.data)


class MeAPIView(PartialUpdateMixin, RetrieveUpdateAPIView):
    """
    Current user endpoint.
    """

    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        user.last_seen = timezone.now()
        user.save()
        return user
