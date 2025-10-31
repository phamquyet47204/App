from django.urls import path
from . import student_views

app_name = 'student'

urlpatterns = [
    # Student profile endpoints
    path('profile/', student_views.get_student_profile, name='get_profile'),
    path('profile/update/', student_views.update_student_profile, name='update_profile'),
    
    # Student schedule
    path('my-schedule/', student_views.get_my_schedule, name='my_schedule'),
    
    # Student registrations
    path('my-registrations/', student_views.get_my_registrations, name='my_registrations'),
    
    # Student document requests
    path('my-document-requests/', student_views.get_my_document_requests, name='my_document_requests'),
    
    # Student notifications
    path('my-notifications/', student_views.get_my_notifications, name='my_notifications'),
    
    # Student tuition fees
    path('my-tuition-fees/', student_views.get_my_tuition_fees, name='my_tuition_fees'),
]