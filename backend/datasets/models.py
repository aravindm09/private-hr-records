from django.db import models
# Create your models here.


class DatasetField(models.Model):

    FIELD_TYPE_CHOICES = [
    ('string', 'String'),
    ('number', 'Number'),  
    ('date', 'Date'),  
    ('email', 'Email'),  
    ('boolean', 'Boolean'),  
    ('choice', 'Choice'),]

    GENERATION_METHOD_CHOICES =[
        ("ctgan","CTGAN"),
        ('faker','Faker'),
        ("ignore","Ignore"),
    ]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='dataset_fields')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    generation_method = models.CharField(max_length=20,choices=GENERATION_METHOD_CHOICES,default="ctgan")

    def __str__(self):
        return self.field_name




