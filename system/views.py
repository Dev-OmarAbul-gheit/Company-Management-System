from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer

class PerformanceReviewViewSet(ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer

    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        review = self.get_object()
        transition = request.data.get('transition')
        
        try:
            if transition == 'schedule_review':
                review.schedule_review()
            elif transition == 'provide_feedback':
                feedback = request.data.get('feedback')
                review.provide_feedback(feedback)
            elif transition == 'submit_for_approval':
                review.submit_for_approval()
            elif transition == 'approve_review':
                review.approve_review()
            elif transition == 'reject_review':
                review.reject_review()
            elif transition == 'resubmit_feedback':
                feedback = request.data.get('feedback')
                review.resubmit_feedback(feedback)
            else:
                return Response({'error': 'Invalid transition'}, status=status.HTTP_400_BAD_REQUEST)
            
            review.save()
            return Response({'status': 'Transition successful', 'state': review.state}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)