from rest_framework import serializers
from .models import GeneratedImage

class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ["id", "user", "prompt", "image_url", "created_at"]
        read_only_fields = ["user", "created_at"]



