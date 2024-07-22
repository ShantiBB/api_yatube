from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from posts.models import Post


class AuthorPermissionMixin(ModelViewSet):
    type_model = None

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return Post.objects.get(pk=post_id)

    def perform_create(self, serializer):
        if self.type_model == 'Post':
            serializer.save(author=self.request.user)
        elif self.type_model == 'Comment':
            serializer.save(
                author=self.request.user, post=self.get_post()
            )

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            if self.type_model == 'Post':
                raise PermissionDenied(
                    'Вы не являетесь автором этого поста!')
            elif self.type_model == 'Comment':
                raise PermissionDenied(
                    'Вы можете изменять только собственные комментарии!'
                )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            if self.type_model == 'Post':
                raise PermissionDenied(
                    'Вы не являетесь автором этого поста!')
            elif self.type_model == 'Comment':
                raise PermissionDenied(
                    'Вы можете удалять только собственные комментарии!'
                )
        instance.delete()

