from django.urls import path
from .views import GenerateDatasetView

urlpatterns =[
    path('generate/<int:pk>/',GenerateDatasetView.as_view(), name="generate")
]