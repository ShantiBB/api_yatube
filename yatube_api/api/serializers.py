from rest_framework.serializers import ModelSerializer, ReadOnlyField

from posts.models import Post, Group, Comment


class AuthorReadOnlySerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')


class PostSerializer(AuthorReadOnlySerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(AuthorReadOnlySerializer):
    post = ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
