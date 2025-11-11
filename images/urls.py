from django.urls import path
from .views import (
    GeneratedImageListCreateView,
    GenerateImageView,
    GeneratedImageDetailView,  # new
    DownloadImageView,         # new
)

urlpatterns = [
    # List all user's images or create a new one
    path("", GeneratedImageListCreateView.as_view(), name="generated-images"),

    # Generate a new image from a text prompt
    path("generate-image/", GenerateImageView.as_view(), name="generate-image"),

    # View, delete, or update a single saved image (by ID)
    path("<int:pk>/", GeneratedImageDetailView.as_view(), name="generated-image-detail"),

    # Download image (optional API endpoint)
    path("<int:pk>/download/", DownloadImageView.as_view(), name="download-image"),
]




