from rest_framework import serializers
from .models import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'review_date', 'feedback', 'review_stage']