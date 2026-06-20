from django.db import models
from projects.models import Project

class UploadedDatasets(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="uploaded_datasets")
    file = models.FileField(upload_to="datasets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0)
    column_count = models.IntegerField(default=0)

    def __str__(self):
        return self.file.name