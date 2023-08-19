from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("practice/:word", views.practice, name="practice"),
    path("practice/reset", views.reset_session, name="practice_reset"),
]