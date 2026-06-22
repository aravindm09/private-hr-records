from django.urls import path
from .views import GenerateDatasetView,GenerateSyntheticDatasetView

urlpatterns =[
    path('generate/<int:pk>/',GenerateDatasetView.as_view(), name="generate"),
    path('synthetic/<int:pk>/',GenerateSyntheticDatasetView.as_view(),name = "synthetic"),
]