from rest_framework import serializers

from posts.models import Post, Group, Comment

AUTHOR = serializers.ReadOnlyField(source='author.username')


class PostSerializer(serializers.ModelSerializer):
    author = AUTHOR

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author, post = AUTHOR, serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
