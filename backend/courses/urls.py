from django.urls import path

from .views import (
    AdminRegistrationWindowView,
    CourseListView,
    RegistrationActionView,
    RegistrationListView,
    RegistrationWindowView,
)

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="courses"),
    path("registrations/", RegistrationListView.as_view(), name="registrations"),
    path("registrations/<int:course_id>/", RegistrationActionView.as_view(), name="registration-action"),
    path("registration-window/", RegistrationWindowView.as_view(), name="registration-window"),
    path("admin/registration-window/", AdminRegistrationWindowView.as_view(), name="admin-registration-window"),
]
