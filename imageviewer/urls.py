from django.urls import path

from . import views

urlpatterns = [
    path("<int:image_id>/", views.image, name="image"),
    path("<int:image_id>/delete/", views.delete, name="delete"),
    path("<int:image_id>/edittags/", views.edittags, name="edittags")
]