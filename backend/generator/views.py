from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from projects.models import Project
from datasets.models import DatasetField
from datasets.serializers import DatasetFieldSerializer
from uploads.models import UploadedDatasets
from .ai_generator import generate_synthetic_data

from faker import Faker
import random
import os 
from django.conf import settings

os.makedirs(os.path.join(settings.MEDIA_ROOT,"synthetic"),exist_ok=True)
fake = Faker()

class GenerateDatasetView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request, pk):
        rows =[]
        project = get_object_or_404(Project,id= pk, user = request.user)
        fields = project.dataset_fields.all()
        serializer = DatasetFieldSerializer(fields, many = True)
        row_count = request.data.get("rows",10)
        for i in range(row_count):
            row ={}
            for field in fields:
                if field.field_type == "email":
                    row[field.field_name] = fake.email()
                elif field.field_type == "string":
                    row[field.field_name] = fake.name()
                elif field.field_type == "number":
                    row[field.field_name] = random.randint(100000,999999)
                elif field.field_type == "date":
                    row[field.field_name] = fake.date()
                elif field.field_type =="boolean":
                    row[field.field_name] = random.choice([True,False])
                else:
                    pass
            rows.append(row)
        return Response(rows)

class GenerateSyntheticDatasetView(APIView):
    permission_classes = [IsAuthenticated]
    def post (self, request, pk):
        project= get_object_or_404(Project,id=pk , user = request.user)
        dataset = project.uploaded_datasets.last()
        if not dataset:
            return Response(
                {"error": "No dataset uploaded"}, status= 400
            )
        rows = request.data.get("rows", 100)
        synthetic_df = generate_synthetic_data(dataset.file.path,rows)
        
        file_name = f"synthetic_project_{project.id}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT,"synthetic",file_name)
        synthetic_df.to_csv(file_path,index=False)
        return Response({"message":"Synthetic dataset generated","file":f"/media/synthetic/{file_name}","rows": len(synthetic_df)})
