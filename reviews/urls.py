from django.urls import path
from . import views
urlpatterns = [
    path("add_review/", views.ReviewView.as_view(),name="add_review"),
    path("show_review/", views.ReviewView.as_view(),name="show_review")
   
]
