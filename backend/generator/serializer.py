from rest_framework import serializers
from .models import SyntheticDataset

class SyntheticDatasetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SyntheticDataset
        fields = [
    "id",
    "file",
    "rows_generated",
    "quality_score",
    "privacy_score",
    "created_at",
]