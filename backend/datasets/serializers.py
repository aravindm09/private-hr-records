from rest_framework import serializers
from .models import DatasetField



class DatasetFieldSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DatasetField
        fields ="__all__"
        read_only_fields =["id","created_at"]
