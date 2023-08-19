from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("practice/reset", views.reset_session, name="practice_reset"),
    path("practice/<str:word_chosen>", views.practice, name="practice"),
]