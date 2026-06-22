from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..projects.models import Project
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = FavoriteSerializer

    def get(self, request):
        qs = (
            Favorite.objects
            .select_related('project', 'project__company', 'project__creator', 'project__primary_category')
            .prefetch_related('project__skills')
            .filter(user=request.user)
            .order_by('-created_at')
        )
        serializer = FavoriteSerializer(qs, many=True)
        return Response(serializer.data)


class FavoriteToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = FavoriteSerializer

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        favorite = Favorite.objects.filter(user=request.user, project=project).first()

        if favorite:
            favorite.delete()
            return Response({'favorited': False}, status=status.HTTP_200_OK)

        Favorite.objects.create(user=request.user, project=project)
        return Response({'favorited': True}, status=status.HTTP_201_CREATED)