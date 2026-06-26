from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from projects.models import Project
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
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        project = get_object_or_404(Project , id =pk , user = request.user)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        file_name = f"synthetic_project_{project.name}_{project.id}_{timestamp}_{unique_id}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT,'synthetic',file_name)
        if not os.path.exists(file_path):
            return Response({'error':"synthetic dataset not found"}, status= 400)
        return Response({"file":f"/media/synthetic/{file_name}"})