from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer
)
from .mixins import AuthorPermissionMixin


class PostViewSet(AuthorPermissionMixin):
    type_model = 'Post'
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.none()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorPermissionMixin):
    type_model = 'Comment'
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.all().filter(post_id=post_id)
