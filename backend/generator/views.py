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
from .models import SyntheticDataset
from .serializer import SyntheticDatasetSerializer
from .analysis import calculate_quality,calculate_privacy

from faker import Faker
import random
import os 
from django.conf import settings
import pandas as pd
import uuid
from datetime import datetime

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
        fields = project.dataset_fields.all()
        dataset = project.uploaded_datasets.last()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        

        if not dataset:
            return Response(
                {"error": "No dataset uploaded"}, status= 400
            )
        rows = request.data.get("rows", 100)
        privacy_level = request.data.get("privacy_level","medium")
        synthetic_df = generate_synthetic_data(dataset.file.path,fields,rows,privacy_level)
        original_columns = pd.read_csv(dataset.file.path,nrows=0).columns
        for col in original_columns:
            if col not in synthetic_df.columns:
                synthetic_df[col]= None
        safe_project_name = (project.name.replace(" ", "_").replace("/", "_").replace("\\", "_"))
        file_name = f"synthetic_project_{safe_project_name}_{project.id}_{timestamp}_{unique_id}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT,"synthetic",file_name)
        synthetic_df.to_csv(file_path,index=False)
        quality_result = calculate_quality(dataset.file.path,file_path)
        privacy_result = calculate_privacy(dataset.file.path,file_path)
        SyntheticDataset.objects.create(project=project,file=f"synthetic/{file_name}",rows_generated = len(synthetic_df),quality_score=quality_result["quality_score"],privacy_score =privacy_result["privacy_score"])
        return Response({"message":"Synthetic dataset generated","file":f"/media/synthetic/{file_name}","rows": len(synthetic_df)})


class DatasetQualityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        project = get_object_or_404(Project, id =pk , user= request.user)
        original_dataset = project.uploaded_datasets.last()
        latest_generation = SyntheticDataset.objects.filter(project=project).order_by("-created_at").first()
        if not latest_generation:
            return Response({"error": "No synthetic dataset generated"},status=400)
        synthetic_file = latest_generation.file.path
        if not os.path.exists(synthetic_file):
            return Response({"error": "Generate synthetic dataset first"},status=400)
        result = calculate_quality(original_dataset.file.path,synthetic_file)
        if latest_generation:
            latest_generation.quality_score = result["quality_score"]
            latest_generation.save()
        return Response(result)

class DatasetPrivacyView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        project = get_object_or_404(Project,id=pk,user=request.user)

        original_dataset = project.uploaded_datasets.last()
        latest_generation = SyntheticDataset.objects.filter(project=project).order_by("-created_at").first()
        if not latest_generation:
            return Response({"error": "No synthetic dataset generated"},status=400)
        

        synthetic_file = latest_generation.file.path
        if not os.path.exists(synthetic_file):
            return Response({"error": "Generate synthetic dataset first"},status=400)
        result = calculate_privacy(original_dataset.file.path,synthetic_file)
        if latest_generation:
            latest_generation.privacy_score = result["privacy_score"]
            latest_generation.save()
        return Response(result)

   
    

class ProjectGenerateHistoryView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request,pk):
        project= get_object_or_404(Project,id=pk,user=request.user)
        generations = SyntheticDataset.objects.filter(project=project).order_by("-created_at")
        serializer =SyntheticDatasetSerializer(generations,many=True)
        return Response(serializer.data)