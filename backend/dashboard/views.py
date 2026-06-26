from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from projects.models import Project
from generator.models import SyntheticDataset
from uploads.models import UploadedDatasets
from datetime import datetime
import uuid
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        total_projects = Project.objects.filter(user = request.user).count()
        total_datasets = UploadedDatasets.objects.filter(project__user=request.user).count()
        return Response({
            "total_projects": total_projects,
            "total_datasets": total_datasets,

        })
    
class DownloadSyntheticDatasetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        project = get_object_or_404(Project,id=pk,user=request.user)

        latest_generation = (SyntheticDataset.objects.filter(project=project).order_by("-created_at").first())
        if not latest_generation:
            return Response({"error": "No synthetic dataset found"},status=400)
        return Response({"file": latest_generation.file.url})
    
class DownloadHistoryDatasetView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request,generation_id):
        generation = get_object_or_404(SyntheticDataset,id =generation_id,project__user = request.user)
        return Response({"file": generation.file.url})