from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer
)
from .mixins import AuthorPermissionMixin


class PostViewSet(AuthorPermissionMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.none()

    def perform_action(
            self, serializer=None, instance=None, action=''
    ):
        if action == 'create':
            serializer.save(author=self.request.user)
        elif action == 'update':
            post = self.get_object()
            if post.author != self.request.user:
                raise PermissionDenied(
                    'Вы не являетесь автором этого поста!')
            serializer.save()
        else:
            if self.request.user != instance.author:
                raise PermissionDenied(
                    'Вы не являетесь автором этого поста!')
            instance.delete()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorPermissionMixin):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.kwargs.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_action(
            self, serializer=None, instance=None, action=''
    ):
        if action == 'create':
            post_id = self.kwargs.get('post_id')
            post = Post.objects.get(pk=post_id)
            serializer.save(author=self.request.user, post=post)
        elif action == 'update':
            if self.request.user != serializer.instance.author:
                raise PermissionDenied(
                    'Вы можете изменять только собственные комментарии!'
                )
            serializer.save()
        else:
            if self.request.user != instance.author:
                raise PermissionDenied(
                    'Вы можете удалять только собственные комментарии!'
                )
