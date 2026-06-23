from django.urls import path
from .views import GenerateDatasetView,GenerateSyntheticDatasetView,DatasetQualityView

urlpatterns =[
    path('generate/<int:pk>/',GenerateDatasetView.as_view(), name="generate"),
    path('synthetic/<int:pk>/',GenerateSyntheticDatasetView.as_view(),name = "synthetic"),
    path('quality/<int:pk>/',DatasetQualityView.as_view(), name="quality_analysis")
]