from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from uploads.models import UploadedDatasets

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        total_projects = Project.objects.filter(user = request.user).count()
        total_datasets = UploadedDatasets.objects.filter(project__user=request.user).count()
        return Response({
            "total_projects": total_projects,
            "total_datasets": total_datasets,

        })