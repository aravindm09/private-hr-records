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
import pandas as pd

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

        if not dataset:
            return Response(
                {"error": "No dataset uploaded"}, status= 400
            )
        rows = request.data.get("rows", 100)
        privacy_level = request.data.get("privacy_level","medium")
        synthetic_df = generate_synthetic_data(dataset.file.path,fields,rows,privacy_level)
        original_df = pd.read_csv(dataset.file.path)
        for col in original_df.columns:
            if col not in synthetic_df.columns:
                synthetic_df[col]= None
        file_name = f"synthetic_project_{project.id}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT,"synthetic",file_name)
        synthetic_df.to_csv(file_path,index=False)
        return Response({"message":"Synthetic dataset generated","file":f"/media/synthetic/{file_name}","rows": len(synthetic_df)})


class DatasetQualityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        project = get_object_or_404(Project, id =pk , user= request.user)
        original_dataset = project.uploaded_datasets.last()
        synthetic_file = os.path.join(settings.MEDIA_ROOT,"synthetic",f"synthetic_project_{project.id}.csv")
        if not os.path.exists(synthetic_file):
            return Response({"error": "Generate synthetic dataset first"},status=400)
        original_df = pd.read_csv(original_dataset.file.path)
        synthetic_df = pd.read_csv(synthetic_file)

        quality_report = {}
        categorial_report ={}
        total_difference = 0
        count = 0 


        numeric_columns = original_df.select_dtypes(include = ["int64","float64"]).columns
        categorial_columns = original_df.select_dtypes(include=["object","bool"]).columns

        for column in numeric_columns:
            original_mean = original_df[column].mean()
            synthetic_mean = synthetic_df[column].mean()
            if original_mean !=0:
                difference_percent = abs((original_mean - synthetic_mean)/original_mean ) * 100
            else : difference_percent =0
            
            if column != 'employee_id':
                total_difference += difference_percent
                count += 1
            quality_report[column]= {
                "original_mean": round(original_mean,2),
                "synthetic_mean": round(synthetic_mean,2),

                "difference_percentage": round(difference_percent,2),
                "original_Min": original_df[column].min(),
                "synthetic_min": synthetic_df[column].min(),
                "original_max": original_df[column].max(),
                "synthetic_max": synthetic_df[column].max(),
                "original_std": round(original_df[column].std(),2),
                "synthetic_std": round(synthetic_df[column].std(),2)
            }

        for column in categorial_columns:
            if column in ["name","email"]:
                continue
            original_distribution = ( original_df[column].value_counts(normalize=True).mul(100).round(2).to_dict())
            synthetic_distribution = (synthetic_df[column].value_counts(normalize=True).mul(100).round(2).to_dict())
            categorial_report[column]= {
                "original": original_distribution,
                "synthetic": synthetic_distribution
            }
        if count > 0:
            average_difference = total_difference/count
        else: average_difference = 0 
        quality_score =max(0,round(100- average_difference,2))
        if quality_score >= 90:
            quality_rating ="Excellent"
        elif quality_score >= 75:
            quality_rating = "Good"
        elif quality_score >=60:
            quality_rating ="Fair"
        else:
            quality_rating="Poor"
        return Response({"original_rows": len(original_df),
                         "synthetic_rows": len(synthetic_df),
                         "original_columns":len(original_df.columns),
                         "synthetic_columns":len(synthetic_df.columns),

                         "quality_score": quality_score,
                         "quality_rating": quality_rating,

                         "quality_metrics": quality_report,
                         "categorial_metrics": categorial_report})
    
class DatasetPrivacyView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        project = get_object_or_404(Project,id=pk,user=request.user)

        original_dataset = project.uploaded_datasets.last()

        synthetic_file = os.path.join(settings.MEDIA_ROOT,'synthetic',f'synthetic_project_{project.id}.csv')

        original_df = pd.read_csv(original_dataset.file.path)

        synthetic_df = pd.read_csv(synthetic_file)

        original_df.columns =(original_df.columns.str.strip().str.lower())

        synthetic_df.columns =(synthetic_df.columns.str.strip().str.lower())

        duplicate_count =0 

        for _,row in synthetic_df.iterrows():
            if original_df.eq(row).all(axis=1).any():
                duplicate_count+=1

        total_rows =len(synthetic_df)

        duplicate_percentage =round((duplicate_count/total_rows)*100,2)

        privacy_score =max(0,round(100 - duplicate_percentage,2))

        if privacy_score>=90:
            privacy_rating ='Excellent'
        elif privacy_score>=75:
            privacy_rating= "Good"
        elif privacy_score>= 60:
            privacy_rating ="Fair"
        else: privacy_rating = 'Poor'

        return Response({
            "total_synthetic_rows": total_rows,
            "duplicate_rows": duplicate_count,
            "duplicate_percentage": duplicate_percentage,

            "privacy_score": privacy_score,
            "privacy_rating": privacy_rating,
            
        })