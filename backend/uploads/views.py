from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from projects.models import Project
from .models import UploadedDatasets
from .serializer import UploadedDatasetSerializer
import pandas as pd


class UploadDatasetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        project = get_object_or_404(Project,id=pk, user=request.user)
        serializer = UploadedDatasetSerializer(data = {"project": project.id,"file": request.FILES.get("file")})
        if serializer.is_valid():
            uploaded_dataset = serializer.save()
            df = pd.read_csv(uploaded_dataset.file.path)
            uploaded_dataset.row_count= len(df)
            uploaded_dataset.column_count= len(df.columns)
            uploaded_dataset.save()
            response_serializer = UploadedDatasetSerializer(uploaded_dataset)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=400)