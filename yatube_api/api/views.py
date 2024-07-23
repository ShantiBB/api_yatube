from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer)
from posts.models import Post, Group, Comment


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied(
                'Вы не являетесь автором этого поста!')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied(
                'Вы не являетесь автором этого поста!')
        instance.delete()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.kwargs.get('post_id')
        return queryset.filter(post_id=post_id)

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(pk=post_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post=self.get_post()
        )

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied(
                'Вы можете изменять только собственные комментарии!')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied(
                'Вы можете удалять только собственные комментарии!')
        instance.delete()
