from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author', 'pub_date', 'id')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'created', 'id', 'post')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate_following(self, value):
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError('Нельзя подписаться на самого себя!')
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and Follow.objects.filter(
            user=request.user, following=data['following']
        ).exists():
            raise serializers.ValidationError('Вы уже подписаны на этого пользователя!')
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
