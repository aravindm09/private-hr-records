from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import DatasetField
from .serializers import DatasetFieldSerializer
from projects.models import Project

class DatasetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        serializer = DatasetFieldSerializer(data = request.data)
        project = get_object_or_404(Project,id =pk,user=request.user)
        if serializer.is_valid():
            serializer.save(project = project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class DatasetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        projects=get_object_or_404(Project,id = pk, user=request.user)
        fields = projects.dataset_fields.all()
        serializer = DatasetFieldSerializer(fields,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DatasetDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        fields=get_object_or_404(DatasetField,id= pk , project__user= request.user)
        serializer = DatasetFieldSerializer(fields)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DatasetUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,pk):
        field = get_object_or_404(DatasetField,id=pk,project__user=request.user)
        serializer = DatasetFieldSerializer(field,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk):
        field = get_object_or_404(DatasetField,id=pk , project__user= request.user)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DatasetFieldUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def put(self, request,pk):
        field = get_object_or_404(DatasetField,id=pk, project__user=request.user)
        seralizer = DatasetFieldSerializer(field,data=request.data, partial=True)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(seralizer.errors,status=400)