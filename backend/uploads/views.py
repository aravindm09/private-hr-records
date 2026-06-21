from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from projects.models import Project
from .models import UploadedDatasets
from datasets.models import DatasetField
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
            preview = df.head(5).to_dict(orient="records")
            uploaded_dataset.row_count= len(df)
            uploaded_dataset.column_count= len(df.columns)
            detected_fields =[]
            for column in df.columns:
                column_name = column.strip().lower()
                if "email" in column_name:
                    field_type = "email"
                elif any(keyword in column_name for keyword in ["date","dob","birth","joining","hire","start","termination","resignation"]):
                    field_type = "date"
                elif pd.api.types.is_bool_dtype(df[column]):
                    field_type="boolean"
                elif pd.api.types.is_numeric_dtype(df[column]):
                    field_type= 'number'
                else:
                    field_type= "string"
                
                if not DatasetField.objects.filter(project=project,field_name=column_name).exists():
                    DatasetField.objects.create(project=project, field_name = column_name, field_type= field_type)
                
                detected_fields.append({
                    "field_name": column_name,
                    "field_type": field_type
                })
            uploaded_dataset.save()
            response_serializer = UploadedDatasetSerializer(uploaded_dataset)
            return Response({"dataset":response_serializer.data,"preview": preview, "fields": detected_fields})
        return Response(serializer.errors, status=400)