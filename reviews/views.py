from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from title_category_genre.models import Title

from . import serializers
from .models import Review
from .permissions import ReviewCommentPermission


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
