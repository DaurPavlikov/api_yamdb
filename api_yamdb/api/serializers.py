from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta():
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request'].method
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title')
        if request == 'POST' and Review.objects.filter(
                                                        title=title_id,
                                                        author=author).exists:
            raise serializers.ValidationError(
                'Вы уже написали отзыв')
        elif request != 'POST':
            return data
        return data
