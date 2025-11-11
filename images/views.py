# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.http import FileResponse, Http404
# from django.conf import settings
# from .models import GeneratedImage
# from .serializers import GeneratedImageSerializer
# import requests
# from io import BytesIO


# # ✅ List + Create
# class GeneratedImageListCreateView(generics.ListCreateAPIView):
#     serializer_class = GeneratedImageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return GeneratedImage.objects.filter(user=self.request.user).order_by("-created_at")

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# # ✅ Retrieve + Delete (for individual images)
# class GeneratedImageDetailView(generics.RetrieveDestroyAPIView):
#     serializer_class = GeneratedImageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return GeneratedImage.objects.filter(user=self.request.user)


# # ✅ Generate image using RapidAPI and save result
# class GenerateImageView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         prompt = request.data.get("prompt")
#         if not prompt:
#             return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

#         RAPIDAPI_KEY = getattr(settings, "RAPIDAPI_KEY", None)
#         if not RAPIDAPI_KEY:
#             return Response({"error": "Missing RapidAPI key in settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         url = "https://chatgpt-42.p.rapidapi.com/texttoimage"
#         payload = {"text": prompt, "width": 512, "height": 512}
#         headers = {
#             "x-rapidapi-key": RAPIDAPI_KEY,
#             "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
#             "Content-Type": "application/json",
#         }

#         try:
#             response = requests.post(url, json=payload, headers=headers)
#             data = response.json()

#             image_url = (
#                 data.get("image_url")
#                 or data.get("url")
#                 or data.get("output_url")
#                 or data.get("generated_image")
#             )

#             if not image_url:
#                 return Response(
#                     {"error": "No image URL found in API response", "details": data},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             generated = GeneratedImage.objects.create(
#                 user=request.user,
#                 prompt=prompt,
#                 image_url=image_url
#             )

#             serializer = GeneratedImageSerializer(generated)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # ✅ Download image endpoint
# class DownloadImageView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             image = GeneratedImage.objects.get(pk=pk, user=request.user)
#         except GeneratedImage.DoesNotExist:
#             raise Http404("Image not found")

#         response = requests.get(image.image_url)
#         if response.status_code != 200:
#             return Response({"error": "Failed to fetch image from source"}, status=400)

#         file_stream = BytesIO(response.content)
#         return FileResponse(file_stream, as_attachment=True, filename=f"image_{pk}.png")



from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.conf import settings
from .models import GeneratedImage
from .serializers import GeneratedImageSerializer
import requests
from io import BytesIO
import mimetypes  # ✅ For detecting correct file extension


# ✅ List + Create
class GeneratedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = GeneratedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GeneratedImage.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ Retrieve + Delete (for individual images)
class GeneratedImageDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = GeneratedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GeneratedImage.objects.filter(user=self.request.user)


# ✅ Generate image using RapidAPI and save result
class GenerateImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        RAPIDAPI_KEY = getattr(settings, "RAPIDAPI_KEY", None)
        if not RAPIDAPI_KEY:
            return Response({"error": "Missing RapidAPI key in settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = "https://chatgpt-42.p.rapidapi.com/texttoimage"
        payload = {"text": prompt, "width": 512, "height": 512}
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()

            image_url = (
                data.get("image_url")
                or data.get("url")
                or data.get("output_url")
                or data.get("generated_image")
            )

            if not image_url:
                return Response(
                    {"error": "No image URL found in API response", "details": data},
                    status=status.HTTP_400_BAD_REQUEST
                )

            generated = GeneratedImage.objects.create(
                user=request.user,
                prompt=prompt,
                image_url=image_url
            )

            serializer = GeneratedImageSerializer(generated)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ Download image endpoint with correct file type
class DownloadImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            image = GeneratedImage.objects.get(pk=pk, user=request.user)
        except GeneratedImage.DoesNotExist:
            raise Http404("Image not found")

        response = requests.get(image.image_url)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch image from source"}, status=400)

        # ✅ Detect correct file extension based on Content-Type
        content_type = response.headers.get("Content-Type", "")
        ext = mimetypes.guess_extension(content_type.split(";")[0]) or ".png"

        file_stream = BytesIO(response.content)

        return FileResponse(
            file_stream,
            as_attachment=True,
            filename=f"image_{pk}{ext}",
            content_type=content_type
        )
