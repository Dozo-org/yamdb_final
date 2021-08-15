from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from title_category_genre.models import Title

from .models import Comment, Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='name', read_only=True,)
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError('It is impossible '
                                      'to create a 2nd review.')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
