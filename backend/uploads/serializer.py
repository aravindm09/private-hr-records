from rest_framework import serializers
from .models import UploadedDatasets

class UploadedDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDatasets
        fields = "__all__"