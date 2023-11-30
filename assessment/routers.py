from rest_framework.routers import DefaultRouter

from assessment.viewsets import QuestionViewSet

assessment_router = DefaultRouter()

assessment_router.register(r"questions", QuestionViewSet)
