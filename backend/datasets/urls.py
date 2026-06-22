from django.urls import path
from .views import (DatasetCreateView,DatasetListView,DatasetDetailView,DatasetUpdateView,DatasetDeleteView,DatasetFieldUpdateView)

urlpatterns=[
            path("create/<int:pk>/", DatasetCreateView.as_view(), name='create_dataset'),
            path("list/<int:pk>/",DatasetListView.as_view(), name='list_dataset'),
            path("detail/<int:pk>/",DatasetDetailView.as_view(),name= "detail_dataset"),
            path("update/<int:pk>/",DatasetUpdateView.as_view(),name= "update_dataset"),
            path("delete/<int:pk>/",DatasetDeleteView.as_view(),name= "delete_dataset"),
            path("fields/<int:pk>/",DatasetFieldUpdateView.as_view(),name = "field_selection")
]