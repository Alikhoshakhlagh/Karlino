from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .serializers import CompanySerializer


class MyCompanyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get(self, request):
        try:
            company = request.user.company
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)

    def post(self, request):
        if hasattr(request.user, 'company'):
            return Response(
                {'detail': 'Company already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        company = get_object_or_404(Company, owner=request.user)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)