from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginViewSet, CourseViewSet, RegistrationViewSet,
    RegistrationPeriodViewSet, StudentViewSet
)

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'registrations', RegistrationViewSet, basename='registrations')
router.register(r'periods', RegistrationPeriodViewSet, basename='periods')
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(router.urls)),
]
