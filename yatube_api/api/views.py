from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Post, Follow, Group
from .serializers import (
    PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
)
from .pagination import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_pagination_class(self):
        has_limit = 'limit' in self.request.query_params
        has_offset = 'offset' in self.request.query_params

        if has_limit or has_offset:
            return PostPagination
        return None

    @property
    def pagination_class(self):
        return self.get_pagination_class()

    def list(self, request, *args, **kwargs):
        no_limit = 'limit' not in request.query_params
        no_offset = 'offset' not in request.query_params

        if no_limit and no_offset:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # Иначе используем стандартный list с пагинацией
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().partial_update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all().order_by('id')  # Сортируем по id

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            self.permission_denied(request, message="У вас недостаточно прав.")
        return super().partial_update(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        following_username = request.data.get('following')
        if following_username == request.user.username:
            return Response(
                {'following': ['Нельзя подписаться на самого себя!']},
                status=400
            )
        return super().create(request, *args, **kwargs)
